import requests
from config import NOTION_TOKEN, NOTION_DATABASE_ID

def export_to_notion(leads: list):
    """Pushes a list of leads to a Notion Database."""
    if not leads:
        return
        
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("Skipping Notion export. NOTION_TOKEN or NOTION_DATABASE_ID is missing.")
        return

    print(f"Exporting {len(leads)} leads to Notion...")

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2026-03-11"
    }

    success_count = 0
    
    for lead in leads:
        # Notion requires specific JSON structure to map to exactly named columns.
        # Make sure your Notion Database has these exact properties (types in parentheses):
        # Name (Title), Subreddit (Rich text), URL (URL), Snippet (Rich text)
        data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {"content": lead["title"][:2000]} # Limit to 2000 chars just in case
                        }
                    ]
                },
                "URL": {
                    "url": lead["url"]
                },
                "Subreddit": {
                    "rich_text": [
                        {
                            "text": {"content": lead.get("subreddit", "UNKNOWN")}
                        }
                    ]
                },
                "Snippet": {
                    "rich_text": [
                        {
                            "text": {"content": lead["body"][:2000]} # Rich text is limited per block
                        }
                    ]
                }
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"Failed to export lead to Notion: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Notion request error: {e}")

    print(f"Successfully exported {success_count} leads to Notion.")
