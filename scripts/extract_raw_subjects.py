import pandas as pd
from src.email_reader import extract_all_emails

def main():
    emails = extract_all_emails(days_back=90, max_results=1000)
    print(f"✅ Correos extraídos: {len(emails)}")

    df = pd.DataFrame(emails)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    df.to_excel("data/raw_emails.xlsx", index=False)
    print("💾 Guardado como raw_emails.xlsx")

if __name__ == "__main__":
    main()
