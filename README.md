# Spotnxt Competitor Intelligence Engine - Meta Ads Library Automation

Develop a Python automation script that searches the Meta Ads Library for a given brand name, applies the required filters, extracts advertisement information, and stores the results in a structured format.

The goal is to build the first version of Spotnxt's Competitor Intelligence Engine.

## Quick Start
```bash
pip install -r requirements.txt
playwright install chromium
python app.py --brand Nike
```

## Expected Workflow Supported
- **Step 1:** Opens the Meta Ads Library (https://www.facebook.com/ads/library)
- **Step 2:** Applies filters (`Country: India`, `Ad Category: All Ads`)
- **Step 3:** Searches using the Brand Name provided by the user.
- **Step 4:** Waits until advertisements are completely loaded and handles loading delays properly.
- **Step 5:** Collects exactly the first 5 advertisements.

## Information Extracted
For every advertisement, the following information is collected:
- **Advertisement Details:** Brand Name, Advertisement Number, Platform (Facebook / Instagram), Ad Status, Ad Started Date
- **Advertisement Content:** Primary Text, Headline, Description, Call To Action
- **Creative Assets:** Advertisement Image URL, Advertisement Video URL (if available)
- **Landing Page:** Landing Page URL
- **Screenshot:** Captures one screenshot of each advertisement (stored in `screenshots/<Brand Name>/ad_x.png`)

## Setup & Installation

### 1. Prerequisites
- Python 3.12+
- PostgreSQL Server (running locally or remotely)
- Google Chrome / Chromium

### 2. Environment Variables
Copy the example environment file and configure it:
```bash
cp .env.example .env
```
Update `.env` with your actual PostgreSQL connection string:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
HEADLESS=True
```

## Command Line Usage

Run the program like this:
```bash
python app.py
```

**Input**
```text
Enter Brand Name
Nike
```

**Output**
```text
Searching Meta Ads Library...
Applying Country Filter...
Applying Ad Category...
Searching Nike...
Collecting advertisements...
Advertisement 1 collected
Advertisement 2 collected
Advertisement 3 collected
Advertisement 4 collected
Advertisement 5 collected
Saving JSON...
Saving Database...
Completed Successfully.
```

## Storage & Output
- **JSON:** A generated `output/output.json` file structured perfectly according to the assignment requirements.
- **Database:** A PostgreSQL table containing 5 records with fields: `id`, `brand_name`, `platform`, `status`, `started_date`, `primary_text`, `headline`, `description`, `cta`, `landing_page`, `image_url`, `video_url`, `screenshot_path`, `scraped_at`.
- **Screenshots:** Folder structure mirroring `screenshots/Nike/ad_1.png` to `ad_5.png`.

## Project Structure
```text
spotnxt-meta-ads/
│
├── app.py               # Main CLI application entry point
├── config.py            # Environment variable configuration
├── scraper.py           # Core Playwright scraping logic
├── extractor.py         # Resilient field extraction logic
├── database.py          # SQLAlchemy engine and session setup
├── models.py            # SQLAlchemy declarative models
├── schemas.py           # Pydantic validation schemas
├── utils.py             # File I/O utilities
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── README.md            # Documentation
├── sql/
│   └── schema.sql       # Raw SQL table creation script
├── output/              # Output JSON directory
└── screenshots/         # Advertisement screenshots directory
```
