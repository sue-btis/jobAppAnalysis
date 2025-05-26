import pandas as pd
from src.email_reader import extract_emails
from src.parser import process_mail_List
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    print("Extracting emails...")
    emails_data = extract_emails(days_back=90)
    email_data = process_mail_List(emails_data)

    if not emails_data:
        print("No emails found")

    print(f"✅ Mails: {len(emails_data)}")

    df = pd.DataFrame(email_data)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    # FILTRO SOLO LOS RELEVANTES
    df = df[df["relevante"] == True]

    output_file = "data/tracker.csv"
    df.to_csv(output_file, index=False)

    print(f"<UNK> Excel file saved to {output_file}")


if __name__ == '__main__':
    main()

