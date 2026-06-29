# Meta Ads Library Scraper

A robust Python automation tool to scrape advertisements from the Meta Ads Library, store data in a PostgreSQL database, and export it to a JSON file.

The scraper collects the first five advertisements from the Meta Ads Library, stores screenshots, saves structured JSON output, and inserts the data into PostgreSQL.

## Usage
```bash
pip install -r requirements.txt
playwright install chromium
python app.py --brand Nike
```

## Features
- **Playwright Automation**: Uses synchronous Playwright with explicit waits and robust locators.
- **Resilient Extraction**: Gracefully handles missing elements (e.g., video URLs or CTAs) by falling back to `null` instead of failing.
- **Data Validation**: Uses Pydantic to strictly validate scraped data against schemas.
- **Database Integration**: Utilizes SQLAlchemy ORM for seamless PostgreSQL insertion.
- **Command-Line Interface**: Supports interactive prompts or command-line arguments (e.g., `--brand Nike`).
- **Progress Tracking**: Includes progress logs and a `tqdm` progress bar.

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
├── utils.py             # File I/O and logging utilities
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── README.md            # Documentation
├── sql/
│   └── schema.sql       # Raw SQL table creation script
├── output/              # Directory for output.json and logs
└── screenshots/         # Directory for advertisement screenshots
```

## Setup & Installation

### 1. Prerequisites
- Python 3.12+
- PostgreSQL Server (running locally or remotely)
- Google Chrome / Chromium

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
Install the default Playwright Chromium browser:
```bash
playwright install chromium
```

### 4. Database Setup
Create a PostgreSQL database for the scraper. The application will automatically initialize the `ads` table schema when run, provided the connection string is valid.

### 5. Environment Variables
Copy the example environment file and configure it:
```bash
cp .env.example .env
```
Update `.env` with your actual PostgreSQL connection string:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
HEADLESS=True
```

## How to Run

You can run the script interactively, and it will prompt you for a brand name:
```bash
python app.py
```
> Example Input: `Nike`

Or you can pass the brand name directly as a command-line argument:
```bash
python app.py --brand "Byju's"
```

## Expected Output

1. **Console**: Progress logs detailing navigation, extraction, and a progress bar for database saving.
2. **Screenshots**: Up to 5 screenshots will be saved in `screenshots/<Brand_Name>/ad_1.png` to `ad_5.png`.
3. **JSON**: An `output/output.json` file will be generated containing the structured data of the extracted ads.
4. **Database**: 5 new records will be inserted into the `ads` table in your PostgreSQL database.
