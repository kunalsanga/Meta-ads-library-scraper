import logging
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from config import HEADLESS
from extractor import extract_ad_details
from utils import get_screenshot_path

logger = logging.getLogger(__name__)

class MetaAdsScraper:
    def __init__(self, brand_name: str):
        self.brand_name = brand_name
        self.base_url = "https://www.facebook.com/ads/library"
        self.max_ads = 5

    def scrape(self):
        """Main scraping workflow."""
        extracted_ads = []
        
        with sync_playwright() as p:
            logger.info(f"Launching Chromium browser (headless={HEADLESS})...")
            browser = p.chromium.launch(headless=HEADLESS, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-US",
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
            )
            page = context.new_page()

            try:
                # 1. Navigate to the ads library
                logger.info(f"Navigating to {self.base_url}")
                page.goto(self.base_url, wait_until="networkidle")
                page.screenshot(path="debug_01_base_url.png")

                # 2. Select Country (India is often the default or needs to be typed, for the sake of the URL we can pass query params)
                # It's much more robust to construct the URL directly if we know the parameters!
                # ?active_status=all&ad_type=all&country=IN&q=Nike&search_type=keyword_unordered
                search_url = f"{self.base_url}/?active_status=all&ad_type=all&country=IN&q={self.brand_name}&search_type=keyword_unordered"
                logger.info(f"Applying filters and searching for '{self.brand_name}' via URL: {search_url}")
                page.goto(search_url, wait_until="networkidle")
                page.screenshot(path="debug_02_search_url.png")

                # Wait for results to load
                # We wait for the ad cards to appear. The div wrapper often changes, but we can look for generic terms.
                logger.info("Waiting for advertisements to load...")
                
                # Check for "0 results"
                try:
                    no_results = page.locator("text='0 results'")
                    if no_results.count() > 0 and no_results.is_visible():
                        logger.warning(f"No results found for brand '{self.brand_name}'.")
                        return extracted_ads
                except Exception:
                    pass

                # Wait for at least one ad container. Often they are grid items.
                # 'div.x1y744je' or similar generic classes wrap individual ads. We can look for the "Library ID" text as an anchor.
                try:
                    page.wait_for_selector("text=Library ID", timeout=15000)
                except PlaywrightTimeout:
                    logger.warning("Timeout waiting for ads to load. UI might have changed or page is slow.")
                
                # Sleep a bit extra for dynamic content (images/videos) to stabilize
                time.sleep(3)
                page.screenshot(path="debug_03_ads_loaded.png")

                # Locate ads
                # A robust way is to find elements containing "Library ID" and step up to their container.
                id_spans = page.locator("span:has-text('Library ID')")
                ad_count = id_spans.count()
                logger.info(f"Found {ad_count} advertisements on the page.")

                limit = min(self.max_ads, ad_count)
                
                for i in range(limit):
                    ad_number = i + 1
                    logger.info(f"Extracting ad {ad_number}/{limit}...")
                    
                    # The actual ad card is 7 levels up from the "Library ID" span
                    ad_element = id_spans.nth(i).locator("xpath=ancestor::div[7]").first
                    
                    # Scroll ad into view to ensure it renders and we can take a good screenshot
                    ad_element.scroll_into_view_if_needed()
                    time.sleep(1) # short pause for images to lazy-load

                    # Extract data
                    details = extract_ad_details(ad_element)
                    details['brand_name'] = self.brand_name
                    details['ad_number'] = ad_number

                    # Screenshot
                    screenshot_path = get_screenshot_path(self.brand_name, ad_number)
                    try:
                        ad_element.screenshot(path=screenshot_path)
                        details['screenshot_path'] = screenshot_path
                        logger.info(f"Saved screenshot for ad {ad_number} to {screenshot_path}")
                    except Exception as e:
                        logger.error(f"Failed to capture screenshot for ad {ad_number}: {e}")
                        details['screenshot_path'] = None

                    extracted_ads.append(details)

            except Exception as e:
                logger.error(f"An error occurred during scraping: {e}")
            finally:
                logger.info("Closing browser...")
                browser.close()

        return extracted_ads
