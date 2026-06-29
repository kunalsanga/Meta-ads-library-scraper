CREATE TABLE IF NOT EXISTS ads (
    id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    ad_number INTEGER NOT NULL,
    platform VARCHAR(255),
    status VARCHAR(100),
    started_date VARCHAR(100),
    primary_text TEXT,
    headline TEXT,
    description TEXT,
    cta VARCHAR(100),
    landing_page TEXT,
    image_url TEXT,
    video_url TEXT,
    screenshot_path VARCHAR(500),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
