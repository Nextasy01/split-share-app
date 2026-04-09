import json
from datetime import datetime
import time

from seleniumbase import SB

from config import (
    USE_MOCK_DATA, 
    TARGET_SUBREDDITS
)

class MockRedditFetcher:
    """Simulates fetching posts from Reddit for testing."""
    
    def fetch_recent_posts(self):
        print("Using MockRedditFetcher: generating sample posts...")
        time.sleep(1) # simulate network delay
        
        mock_posts = [
            {
                "id": "mock_id_1",
                "source": "Reddit",
                "subreddit": "Coachella",
                "title": "Looking to split an Airbnb weekend 1!",
                "body": "Hey guys, our group had a few dropouts. We have 2 spots left in our Airbnb in Palm Springs. Looking to split costs evenly.",
                "url": "https://reddit.com/r/Coachella/comments/mock_id_1",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return mock_posts
    
    def close(self):
        pass

class SeleniumRedditFetcher:
    """Fetches real posts using SeleniumBase UC Mode to bypass Cloudflare and parse JSON."""
    
    def __init__(self):
        self.sb = None
        self.driver_context = None

    def fetch_recent_posts(self):
        results = []
        print("Connecting to Reddit using Stealth Browser (SeleniumBase UC)...")
        
        # We start the browser context manually
        with SB(uc=True, headless=True) as sb:
            for sub in TARGET_SUBREDDITS:
                try:
                    url = f"https://www.reddit.com/r/{sub}/new.json"
                    print(f"Fetching {url}")
                    sb.uc_open_with_reconnect(url, reconnect_time=4)
                    
                    # Sometimes reddit returns raw json in a <pre> tag, sometimes in <body>
                    # We will extract the text of the body tag
                    json_text = sb.get_text("body")
                    
                    if not json_text or not json_text.strip().startswith("{"):
                        print(f"Could not read JSON from {url}. Cloudflare might be visible.")
                        continue
                        
                    data = json.loads(json_text)
                    posts = data.get("data", {}).get("children", [])
                    
                    for item in posts:
                        post_data = item.get("data", {})
                        
                        title = post_data.get("title", "")
                        body = post_data.get("selftext", "")
                        url_segment = post_data.get("permalink", "")
                        created_utc = post_data.get("created_utc", 0)
                        
                        results.append({
                            "id": f"reddit_{post_data.get('id')}",
                            "source": "Reddit",
                            "subreddit": sub,
                            "title": title,
                            "body": body,
                            "url": f"https://reddit.com{url_segment}",
                            "timestamp": datetime.fromtimestamp(created_utc).isoformat() if created_utc else datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    print(f"Error fetching from r/{sub}: {e}")
                    
        return results

def get_fetcher():
    if USE_MOCK_DATA:
        return MockRedditFetcher()
    return SeleniumRedditFetcher()
