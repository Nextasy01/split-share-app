from fetcher import get_fetcher
from analyzer import analyze_posts
from storage import init_db, save_leads, get_all_leads
from notion_export import export_to_notion

def main():
    print("--- Starting Growth Engine Prototype ---")
    
    # 1. Initialize Storage
    init_db()
    
    # 2. Get the appropriate fetcher (Mock vs Real) based on config.py
    fetcher = get_fetcher()
    
    # 3. Retrieve posts (Signals)
    posts = fetcher.fetch_recent_posts()
    
    if not posts:
        print("No posts fetched. Exiting.")
        return

    # 4. Analyze and filter posts
    leads = analyze_posts(posts)
    
    # 5. Store the flagged posts
    new_leads = save_leads(leads)
    
    # 6. Export new leads to Notion immediately
    export_to_notion(new_leads)
    
    # 7. Verify by printing what's in the DB
    print("\n--- Current Leads in Database ---")
    all_leads = get_all_leads()
    for l in all_leads:
        print(f"[{l['subreddit']}] {l['title']} -> {l['url']}")

if __name__ == "__main__":
    main()
