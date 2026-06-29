import logging
from playwright.sync_api import Locator

logger = logging.getLogger(__name__)

def safe_extract_text(locator: Locator, selector: str = None) -> str | None:
    """Extracts text content gracefully, returning None if not found."""
    try:
        target = locator.locator(selector) if selector else locator
        if target.count() > 0:
            return target.first.inner_text().strip()
    except Exception as e:
        logger.debug(f"Failed to extract text for {selector}: {e}")
    return None

def safe_extract_attribute(locator: Locator, attribute: str, selector: str = None) -> str | None:
    """Extracts an attribute gracefully, returning None if not found."""
    try:
        target = locator.locator(selector) if selector else locator
        if target.count() > 0:
            return target.first.get_attribute(attribute)
    except Exception as e:
        logger.debug(f"Failed to extract attribute {attribute} for {selector}: {e}")
    return None

def extract_ad_details(ad_element: Locator) -> dict:
    """
    Extracts all required fields from a single ad element.
    Uses resilient techniques and graceful fallbacks.
    """
    details = {}

    # 1. Header Information (Status, Started Date, Platforms)
    details['status'] = None
    details['started_date'] = None
    details['platform'] = None
    try:
        header = ad_element.locator("> div").first
        if header.count() > 0:
            header_text = header.inner_text().split('\n')
            header_text = [t.strip() for t in header_text if t.strip() and t.strip() != '\u200b']
            
            for text in header_text:
                if text in ["Active", "Inactive"]:
                    details['status'] = text
                elif " - " in text or "Started running on" in text or (len(text.split()) > 2 and any(month in text for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])):
                    # Very likely the date string
                    details['started_date'] = text.replace("Started running on ", "").strip()
    except Exception as e:
        logger.debug(f"Failed to extract header: {e}")

    # Fallback for Platform using HTML scan
    platforms = []
    try:
        html = ad_element.inner_html().lower()
        if 'facebook' in html or 'fbcdn' in html: platforms.append("Facebook")
        if 'instagram' in html: platforms.append("Instagram")
        if 'messenger' in html: platforms.append("Messenger")
        if 'audience network' in html: platforms.append("Audience Network")
        platforms = list(set(platforms))
    except Exception:
        pass
    details['platform'] = ", ".join(platforms) if platforms else None

    # 2. Primary Text
    details['primary_text'] = safe_extract_text(ad_element, "div[style*='white-space: pre-wrap']")
    if not details['primary_text']:
         details['primary_text'] = safe_extract_text(ad_element, "div[style*='white-space:pre-wrap']")

    # 3. Media (Image and Video URLs)
    details['image_url'] = None
    try:
        images = ad_element.locator("img")
        if images.count() > 1:
            details['image_url'] = images.nth(1).get_attribute("src")
        elif images.count() == 1:
            details['image_url'] = images.nth(0).get_attribute("src")
    except Exception:
        pass
        
    details['video_url'] = safe_extract_attribute(ad_element, "src", "video")

    # 4. Landing Page, Headline, Description, CTA
    details['headline'] = None
    details['description'] = None
    details['cta'] = None
    details['landing_page'] = None
    try:
        links = ad_element.locator("a[target='_blank']")
        if links.count() > 1:
            lp_link = links.last
            details['landing_page'] = lp_link.get_attribute("href")
            
            lp_texts = lp_link.inner_text().split('\n')
            lp_texts = [t.strip() for t in lp_texts if t.strip() and t.strip() != '\u200b']
            
            if len(lp_texts) >= 3:
                details['headline'] = lp_texts[0]
                details['description'] = lp_texts[1]
                details['cta'] = lp_texts[2]
            elif len(lp_texts) == 2:
                details['headline'] = lp_texts[0]
                details['cta'] = lp_texts[1]
            elif len(lp_texts) == 1:
                details['cta'] = lp_texts[0]
    except Exception as e:
        logger.debug(f"Failed to extract landing page details: {e}")

    # Final fallback for CTA if the above fails
    if not details['cta']:
        cta_locators = [
            "div[role='button']:has-text('Shop Now')",
            "div[role='button']:has-text('Learn More')",
            "div[role='button']:has-text('Sign Up')",
            "div[role='button']:has-text('Apply Now')",
            "div[role='button']:has-text('Book Now')",
            "div.x1q0g3np.x1a02dak"
        ]
        for loc in cta_locators:
            cta_text = safe_extract_text(ad_element, loc)
            if cta_text and len(cta_text) < 30:
                details['cta'] = cta_text
                break

    return details
