import logging
import json
import os
from config import OUTPUT_DIR, SCREENSHOTS_DIR

def setup_logging():
    """Sets up console and file logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    log_file = os.path.join(OUTPUT_DIR, 'scraper.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def save_json(data: list, filename: str = "output.json"):
    """Saves the extracted data to a JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save JSON: {e}")

def get_screenshot_path(brand_name: str, ad_number: int) -> str:
    """Generates the file path for a screenshot."""
    brand_dir = os.path.join(SCREENSHOTS_DIR, brand_name.replace(" ", "_"))
    os.makedirs(brand_dir, exist_ok=True)
    return os.path.join(brand_dir, f"ad_{ad_number}.png")
