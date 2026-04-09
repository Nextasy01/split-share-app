# Split-Stay Growth Engine

A Python-based growth engine prototype that silently scrapes accommodation sharing requests (e.g. users looking to split Airbnb/Hotel costs) from Reddit using stealth browser automation, filters the leads using keyword intent, and syncs them directly to a Notion Database.

## Features
- **Cloudflare Bypass:** Uses [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) (UC Mode) to scrape Reddit `.json` footprints without triggering bot protections or requiring API keys.
- **Intent Analysis:** Filters out irrelevant posts using a predefined list of intent and exclusion keywords.
- **SQLite Caching:** Stores all leads locally in `leads.db` to prevent processing and pushing duplicates.
- **Notion Integration:** Automatically pushes newly captured, deduplicated leads into a designated Notion Database CRM.

## Prerequisites
- Python 3.8+
- Google Chrome (required for SeleniumBase)
- A Notion Workspace

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nextasy01/split-share-app.git
   cd split-share-app
   ```

2. **Set up a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Rename `.env.example` to `.env`.
   ```bash
   # Windows
   copy .env.example .env
   # Mac/Linux
   cp .env.example .env
   ```

## Connecting Notion
1. Go to [Notion My Integrations](https://www.notion.so/my-integrations) and create a new integration.
2. Copy your **Internal Integration Secret** and paste it into `.env` under `NOTION_TOKEN`.
3. In your Notion workspace, create a **Full-Page Database** with the following column structure:
   - `Name` (Type: Title)
   - `URL` (Type: URL)
   - `Subreddit` (Type: Text)
   - `Snippet` (Type: Text)
4. Open the `...` menu in the top right of your database page, go to **Add connections**, and invite the integration you created in step 1.
5. Copy the Database ID from the URL (the 32-character string before the `?v=`) and paste it into `.env` under `NOTION_DATABASE_ID`.

## Usage

Simply run the main orchestrator script:
```bash
python main.py
```

Settings like the targeted subreddits, intent keywords, and mock data toggles can be adjusted inside `config.py`.
