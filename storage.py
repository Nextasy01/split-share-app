import sqlite3
from config import SQLITE_DB_PATH

def init_db():
    """Initializes the SQLite database & table."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            source TEXT,
            subreddit TEXT,
            title TEXT,
            body TEXT,
            url TEXT,
            timestamp TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {SQLITE_DB_PATH}")

def save_leads(leads: list) -> list:
    """Saves a list of lead dictionaries into the SQLite database.
    Returns a list of leads that were NEWLY inserted (skipping duplicates)."""
    new_leads = []
    if not leads:
        return new_leads
        
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    for lead in leads:
        try:
            # Basic Insert or Ignore so we don't save duplicates
            cursor.execute('''
                INSERT OR IGNORE INTO leads (id, source, subreddit, title, body, url, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead['id'],
                lead['source'],
                lead.get('subreddit', 'UNKNOWN'),
                lead['title'],
                lead['body'],
                lead['url'],
                lead['timestamp'],
                lead['status']
            ))
            
            # Check if a row was actually inserted
            if cursor.rowcount > 0:
                new_leads.append(lead)
                
        except Exception as e:
            print(f"Failed to save lead {lead['id']}: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"Saved {len(new_leads)} new leads to the database.")
    return new_leads

def get_all_leads():
    """Helper to query all leads for testing."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM leads ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
