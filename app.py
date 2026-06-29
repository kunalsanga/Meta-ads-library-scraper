import argparse
import logging
from tqdm import tqdm
from utils import setup_logging, save_json
from database import init_db, SessionLocal
from models import Ad as AdModel
from schemas import AdSchema
from scraper import MetaAdsScraper
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Meta Ads Library Scraper")
    parser.add_argument("--brand", type=str, help="Brand name to search for (e.g., 'Nike')")
    args = parser.parse_args()

    brand_name = args.brand
    if not brand_name:
        brand_name = input("Enter Brand Name\n").strip()
    
    if not brand_name:
        print("Brand name cannot be empty.")
        return

    init_db()

    scraper = MetaAdsScraper(brand_name)
    
    # Scrape the ads
    raw_ads = scraper.scrape()
    
    if not raw_ads:
        print("No advertisements found.")
        return

    validated_ads = []
    validated_ads = []
    
    for raw_ad in raw_ads:
        try:
            # 1. Validate data using Pydantic
            ad_schema = AdSchema(**raw_ad)
            ad_data = ad_schema.model_dump()
            validated_ads.append(ad_data)
        except ValidationError as e:
            pass
        except Exception as e:
            pass

    # Save to output.json
    if validated_ads:
        print("Saving JSON...")
        # Prepare json-friendly data
        json_ads = []
        for ad in validated_ads:
            ad_copy = ad.copy()
            if 'scraped_at' in ad_copy:
                ad_copy['scraped_at'] = ad_copy['scraped_at'].isoformat()
            if 'screenshot_path' in ad_copy:
                ad_copy['screenshot'] = ad_copy.pop('screenshot_path')
            # Remove id and scraped_at as they are not in the assignment example
            ad_copy.pop('id', None)
            ad_copy.pop('scraped_at', None)
            ad_copy.pop('brand_name', None)
            json_ads.append(ad_copy)
            
        final_json = {
            "brand_name": brand_name,
            "ads": json_ads
        }
        
        save_json(final_json, "output.json")
        
        # Now print Saving Database and commit
        print("Saving Database...")
        
        db = SessionLocal()
        try:
            for ad_data in validated_ads:
                db_ad = AdModel(**ad_data)
                db.add(db_ad)
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()
            
        print("Completed Successfully.")



if __name__ == "__main__":
    main()
