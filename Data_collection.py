import requests
import time
import json
import os
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

collected_data = []

def fetch_top_story_ids():
    print("🚀 Fetching top stories...")
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)
        response.raise_for_status()
        ids = response.json()[:100]   # 🔥 reduced for speed
        print(f"✅ Got {len(ids)} story IDs\n")
        return ids
    except Exception as e:
        print("❌ Error fetching top stories:", e)
        return []

def fetch_story(story_id):
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords):
            return category
    return None

def main():
    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("❌ No story IDs found. Exiting...")
        return

    category_count = {cat: 0 for cat in categories}

    print("🔄 Starting processing...\n")

    for category in categories:
        print(f"\n📂 CATEGORY: {category.upper()}")

        for i, story_id in enumerate(story_ids):

            if category_count[category] >= 25:
                print(f"✔ Done: 25 stories collected for {category}")
                break

            # 👇 SHOW PROGRESS MORE FREQUENTLY
            print(f"➡ Checking story {i+1}/{len(story_ids)}", end="\r")

            story = fetch_story(story_id)
            if not story:
                continue

            title = story.get("title", "")
            if not title:
                continue

            if get_category(title) == category:
                print(f"\n✅ Added: {title[:50]}...")

                collected_data.append({
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                category_count[category] += 1

        print("\n⏳ Waiting 2 seconds...")
        time.sleep(2)

    # Create folder
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print("\n==============================")
    print(f"🎯 Total Collected: {len(collected_data)} stories")
    print(f"📁 File saved at: {filename}")
    print("==============================")

if __name__ == "__main__":
    main()