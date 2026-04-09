import pandas as pd
import os
import json

DATA_FOLDER = "data"

def get_latest_json_file():
    """Find latest JSON file safely"""

    # ✅ Create folder if not exists
    if not os.path.exists(DATA_FOLDER):
        print("⚠️ 'data' folder not found. Creating it...")
        os.makedirs(DATA_FOLDER)
        print("❌ No JSON file found. Please run Task 1 first.\n")
        return None

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]

    if not files:
        print("❌ No JSON files found in 'data' folder.")
        print("👉 Run Task 1 first to generate JSON file.\n")
        return None

    files.sort(reverse=True)
    latest_file = os.path.join(DATA_FOLDER, files[0])

    print(f"📂 Found file: {latest_file}")
    return latest_file


def load_json(file_path):
    """Load JSON data safely"""
    print("\n📥 Loading JSON data...")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"✅ Loaded {len(data)} records")
        return data

    except Exception as e:
        print("❌ Error reading JSON:", e)
        return []


def clean_data(df):
    """Clean dataset"""
    print("\n🧹 Cleaning data...")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["post_id"])
    print(f"✔ Removed {before - len(df)} duplicate rows")

    # Fill missing values
    df["author"] = df["author"].fillna("unknown")
    df["score"] = df["score"].fillna(0)
    df["num_comments"] = df["num_comments"].fillna(0)

    # Remove rows without title
    df = df[df["title"].notna()]

    print(f"✔ Final records after cleaning: {len(df)}")

    return df


def save_csv(df, json_file):
    """Save cleaned data to CSV"""
    csv_file = json_file.replace(".json", ".csv")

    print("\n💾 Saving CSV file...")
    df.to_csv(csv_file, index=False, encoding="utf-8")

    print(f"✅ CSV saved at: {csv_file}")


def main():
    print("🚀 Starting Data Processing...\n")

    json_file = get_latest_json_file()

    if not json_file:
        return

    data = load_json(json_file)

    if not data:
        return

    print("\n🔄 Converting to DataFrame...")
    df = pd.DataFrame(data)
    print(f"📊 Data shape: {df.shape}")

    df = clean_data(df)

    save_csv(df, json_file)

    print("\n==============================")
    print("🎯 Data processing completed successfully!")
    print("==============================")


if __name__ == "__main__":
    main()