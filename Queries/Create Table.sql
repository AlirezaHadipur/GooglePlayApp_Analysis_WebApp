CREATE TABLE google_play_apps (
    app_name VARCHAR(255) NOT NULL,
    app_id VARCHAR(255) PRIMARY KEY,
    category VARCHAR(255),
    rating FLOAT,
    rating_count INT,
    size_of_app VARCHAR(50),
    minimum_android VARCHAR(50),
    developer_id VARCHAR(255),
    developer_website VARCHAR(255),
    developer_email VARCHAR(255),
    released VARCHAR(50),
    last_updated VARCHAR(50),
    content_rating VARCHAR(50),
    privacy_policy VARCHAR(20000),
    ad_supported BOOLEAN,
    in_app_purchases BOOLEAN,
    editors_choice BOOLEAN,
    install_count FLOAT,
    price_usd FLOAT
);

-- Example indexing for optimizing searches:
CREATE INDEX idx_category ON google_play_apps (category);
CREATE INDEX idx_rating ON google_play_apps (rating);
CREATE INDEX idx_install_count ON google_play_apps (install_count);
CREATE INDEX idx_price_usd ON google_play_apps (price_usd);
CREATE INDEX idx_editors_choice ON google_play_apps (editors_choice);
CREATE INDEX idx_content_rating ON google_play_apps (content_rating);
CREATE INDEX idx_last_update ON google_play_apps (last_updated);
CREATE INDEX idx_released ON google_play_apps (released)