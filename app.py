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
        brand_name = input("Enter Brand Name:\n").strip()
    
    if not brand_name:
        logger.error("Brand name cannot be empty.")
        return

    logger.info("Initializing database...")
    init_db()

    scraper = MetaAdsScraper(brand_name)
    logger.info(f"Starting scrape for brand: {brand_name}")
    
    # Scrape the ads
    raw_ads = scraper.scrape()
    
    if not raw_ads:
        logger.warning("No advertisements were extracted.")
        return

    validated_ads = []
    
    logger.info("Validating and saving data to database...")
    db = SessionLocal()
    try:
        # Use tqdm to show progress for data processing and database insertion
        for raw_ad in tqdm(raw_ads, desc="Saving Ads"):
            try:
                # 1. Validate data using Pydantic
                ad_schema = AdSchema(**raw_ad)
                ad_data = ad_schema.model_dump()
                validated_ads.append(ad_data)
                
                # 2. Insert into SQLAlchemy Model
                db_ad = AdModel(**ad_data)
                db.add(db_ad)
            except ValidationError as e:
                logger.error(f"Data validation error for ad {raw_ad.get('ad_number')}: {e}")
            except Exception as e:
                logger.error(f"Error processing ad {raw_ad.get('ad_number')}: {e}")
        
        db.commit()
        logger.info("Data successfully committed to PostgreSQL.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to commit transactions to database: {e}")
    finally:
        db.close()

    # Save to output.json
    if validated_ads:
        # Convert datetime to ISO format strings for JSON serialization
        for ad in validated_ads:
            if 'scraped_at' in ad:
                ad['scraped_at'] = ad['scraped_at'].isoformat()
        
        save_json(validated_ads, "output.json")
        logger.info("Process completed successfully. Check the 'output' and 'screenshots' folders.")

if __name__ == "__main__":
    main()
