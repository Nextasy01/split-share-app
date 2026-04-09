from config import INTENT_KEYWORDS, EXCLUDE_KEYWORDS

def is_accommodation_intent(post_data: dict) -> bool:
    """
    Very basic NLP/Keyword matching engine.
    Returns True if the post looks like an accommodation sharing intent.
    """
    
    text_to_analyze = (post_data.get('title', '') + " " + post_data.get('body', '')).lower()
    
    # 1. Check for exclusion words first (e.g., they just want a ride)
    for excl in EXCLUDE_KEYWORDS:
        if excl in text_to_analyze:
            return False
            
    # 2. Check for intent keywords
    matched_keywords = [kw for kw in INTENT_KEYWORDS if kw in text_to_analyze]
    
    # Require at least one keyword. 
    # To reduce false positives in a real system, you might require 2 matches (e.g. "split" AND "airbnb")
    if len(matched_keywords) > 0:
        # Give some feedback on console
        print(f"  [!] Signal Detected in post: '{post_data['title'][:30]}...' -> Matched keywords: {matched_keywords}")
        return True
        
    return False

def analyze_posts(posts: list) -> list:
    """Filters a list of posts, returning only the actionable leads."""
    leads = []
    print(f"Analyzing {len(posts)} posts for intent...")
    for post in posts:
        if is_accommodation_intent(post):
            post['status'] = 'FLAGGED'
            leads.append(post)
    print(f"Identified {len(leads)} potential leads.")
    return leads
