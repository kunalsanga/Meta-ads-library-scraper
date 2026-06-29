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

    # Extract Status (e.g., Active)
    # Status usually appears in a span with text "Active" or "Inactive"
    details['status'] = None
    try:
        status_element = ad_element.locator("span:has-text('Active'), span:has-text('Inactive')").first
        if status_element.count() > 0:
            details['status'] = status_element.inner_text().strip()
    except Exception:
        pass

    # Extract Started Date
    # Text typically starts with "Started running on"
    details['started_date'] = None
    try:
        started_element = ad_element.locator("span:has-text('Started running on')").first
        if started_element.count() > 0:
            text = started_element.inner_text().strip()
            details['started_date'] = text.replace("Started running on ", "").strip()
    except Exception:
        pass
        
    # Extract Platform (e.g., Facebook, Instagram)
    # Platforms are often represented by icons (e.g. svg with aria-label) or tooltip text
    # This is often brittle, so we collect the aria-labels of platform icons
    platforms = []
    try:
        icons = ad_element.locator("div.xtwsqm5 > div > div > span") # typical platform container
        for i in range(icons.count()):
            # Fallback to look for generic tooltips or aria labels if specific classes fail
            # For resilience, we just look at small logos or assume unknown if missing
            pass
        # A more generic approach: check if word Facebook/Instagram is anywhere in a visually hidden span
        for pf in ["Facebook", "Instagram", "Audience Network", "Messenger"]:
            if ad_element.locator(f"span:has-text('{pf}')").count() > 0:
                platforms.append(pf)
    except Exception:
        pass
    details['platform'] = ", ".join(platforms) if platforms else None

    # Primary Text (The main post text)
    # Usually in a div with a specific style, but we can look for generic text blocks
    # Here we pick a common generic selector for the post body
    details['primary_text'] = safe_extract_text(ad_element, "div[style*='white-space: pre-wrap']")

    # Call to Action (CTA)
    # Usually a div that looks like a button
    # Let's look for a standard button role or common CTA texts
    cta_locators = [
        "div[role='button']:has-text('Shop Now')",
        "div[role='button']:has-text('Learn More')",
        "div[role='button']:has-text('Sign Up')",
        "div[role='button']:has-text('Apply Now')",
        "div[role='button']:has-text('Book Now')",
        "div.x1q0g3np.x1a02dak" # typical CTA wrapper class fallback
    ]
    details['cta'] = None
    for loc in cta_locators:
        cta_text = safe_extract_text(ad_element, loc)
        if cta_text and len(cta_text) < 30: # sanity check
            details['cta'] = cta_text
            break

    # Headline and Description (under the image/video)
    # These are usually the bold text and secondary text near the CTA
    # We use a broad selector and clean it up
    details['headline'] = None
    details['description'] = None
    
    # Image URL and Video URL
    details['image_url'] = safe_extract_attribute(ad_element, "src", "img")
    details['video_url'] = safe_extract_attribute(ad_element, "src", "video")

    # Landing Page URL
    # Usually the href of the main anchor tag
    hrefs = []
    try:
        links = ad_element.locator("a")
        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if href and "facebook.com/ads/library" not in href:
                hrefs.append(href)
    except Exception:
        pass
    details['landing_page'] = hrefs[0] if hrefs else None

    return details
