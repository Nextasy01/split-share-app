import os
from dotenv import load_dotenv

load_dotenv()

# Flag to use mock data instead of real reddit scraping 
# Set to False to run the SeleniumBase scraper live
USE_MOCK_DATA = False

# Target communities/forums
TARGET_SUBREDDITS = [
    "Coachella",
    "Lollapalooza",
    "Tomorrowland",
    "festivals",
    "travel"
]

# Simple keywords to detect someone looking for accommodation sharing
INTENT_KEYWORDS = [
    "split",
    "share",
    "room",
    "airbnb",
    "hotel",
    "accommodation",
    "staying",
    "looking for a place",
    "need a room"
]

# Keywords that help disqualify (e.g. people offering a ride instead)
EXCLUDE_KEYWORDS = [
    "ride",
    "carpool",
    "driving"
]

# Notion API Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")

# Storage
SQLITE_DB_PATH = "leads.db"
