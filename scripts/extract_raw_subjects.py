import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.email_reader import extract_all_subjects_only

def main():
    emails = extract_all_subjects_only(days_back=90, max_results=2000)
    print(f"✅ Asuntos extraídos: {len(emails)}")

    df = pd.DataFrame(emails)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    df.to_csv("data/raw_subjects.csv", index=False)
    print("💾 Guardado como data/raw_subjects.csv")

if __name__ == "__main__":
    main()

