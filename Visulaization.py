import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FOLDER = "data"

def get_latest_csv():
    """Get latest CSV file"""
    if not os.path.exists(DATA_FOLDER):
        print("❌ 'data' folder not found")
        return None

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    if not files:
        print("❌ No CSV file found. Run Task 2/3 first.")
        return None

    files.sort(reverse=True)
    return os.path.join(DATA_FOLDER, files[0])


def main():
    print("🚀 Starting Visualization...\n")

    csv_file = get_latest_csv()
    if not csv_file:
        return

    print(f"📂 Loading file: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} records\n")

    sns.set_style("whitegrid")
    plt.rcParams["figure.figsize"] = (10,6)

    # -------------------------------
    # 1. Posts per category
    # -------------------------------
    plt.figure()
    category_counts = df["category"].value_counts()
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.title("Number of Posts per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Posts")
    for i, v in enumerate(category_counts.values):
        plt.text(i, v+0.5, str(v), ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig("data/posts_per_category.png")
    print("💾 Saved: data/posts_per_category.png")

    # -------------------------------
    # 2. Average score per category
    # -------------------------------
    plt.figure()
    avg_score = df.groupby("category")["score"].mean().sort_values(ascending=False)
    sns.barplot(x=avg_score.index, y=avg_score.values, palette="magma")
    plt.title("Average Score per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")
    for i, v in enumerate(avg_score.values):
        plt.text(i, v+0.5, f"{v:.1f}", ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig("data/avg_score_per_category.png")
    print("💾 Saved: data/avg_score_per_category.png")

    # -------------------------------
    # 3. Total comments per category
    # -------------------------------
    plt.figure()
    total_comments = df.groupby("category")["num_comments"].sum().sort_values(ascending=False)
    sns.barplot(x=total_comments.index, y=total_comments.values, palette="coolwarm")
    plt.title("Total Comments per Category")
    plt.xlabel("Category")
    plt.ylabel("Total Comments")
    for i, v in enumerate(total_comments.values):
        plt.text(i, v+0.5, str(v), ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig("data/total_comments_per_category.png")
    print("💾 Saved: data/total_comments_per_category.png")

    # -------------------------------
    # 4. Top 5 highest scored posts
    # -------------------------------
    top_posts = df.sort_values("score", ascending=False).head(5)
    plt.figure()
    sns.barplot(x="score", y="title", data=top_posts, palette="plasma")
    plt.title("Top 5 Highest Scored Posts")
    plt.xlabel("Score")
    plt.ylabel("Post Title")
    plt.tight_layout()
    plt.savefig("data/top5_posts.png")
    print("💾 Saved: data/top5_posts.png")

    print("\n==============================")
    print("🎯 Visualization completed! Check the 'data/' folder for PNGs.")
    print("==============================")
    plt.show()  # optional: display plots interactively


if __name__ == "__main__":
    main()