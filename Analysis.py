import pandas as pd
import numpy as np
import os

DATA_FOLDER = "data"

def get_latest_csv():
    """Get latest CSV file"""
    if not os.path.exists(DATA_FOLDER):
        print("❌ 'data' folder not found")
        return None

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

    if not files:
        print("❌ No CSV file found. Run Task 2 first.")
        return None

    files.sort(reverse=True)
    return os.path.join(DATA_FOLDER, files[0])


def main():
    print("🚀 Starting Data Analysis...\n")

    csv_file = get_latest_csv()
    if not csv_file:
        return

    print(f"📂 Loading file: {csv_file}")
    df = pd.read_csv(csv_file)

    print(f"✅ Loaded {len(df)} records\n")

    # -------------------------------
    # 1. Total posts per category
    # -------------------------------
    print("📊 Posts per category:")
    posts_per_category = df["category"].value_counts()
    print(posts_per_category, "\n")

    # -------------------------------
    # 2. Average score per category
    # -------------------------------
    print("⭐ Average score per category:")
    avg_score = df.groupby("category")["score"].mean()
    print(avg_score, "\n")

    # -------------------------------
    # 3. Top 5 highest scored posts
    # -------------------------------
    print("🏆 Top 5 highest scored posts:")
    top_posts = df.sort_values(by="score", ascending=False).head(5)
    print(top_posts[["title", "score", "category"]], "\n")

    # -------------------------------
    # 4. Total comments per category
    # -------------------------------
    print("💬 Total comments per category:")
    total_comments = df.groupby("category")["num_comments"].sum()
    print(total_comments, "\n")

    # -------------------------------
    # 5. Most active author
    # -------------------------------
    print("👤 Most active author:")
    most_active = df["author"].value_counts().idxmax()
    count = df["author"].value_counts().max()
    print(f"{most_active} ({count} posts)\n")

    # -------------------------------
    # 6. NumPy usage (important!)
    # -------------------------------
    print("📈 NumPy Insights:")

    scores = df["score"].to_numpy()

    print(f"Max score: {np.max(scores)}")
    print(f"Min score: {np.min(scores)}")
    print(f"Average score: {np.mean(scores):.2f}")
    print(f"Standard deviation: {np.std(scores):.2f}")

    print("\n==============================")
    print("🎯 Analysis completed!")
    print("==============================")


if __name__ == "__main__":
    main()