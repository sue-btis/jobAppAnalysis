import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import datetime

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'josuee152@gmail.com'
APP_PASSWORD = 'ultczlbmnqkgrumj'
KEYWORDS = ["application", "interview", "offer", "recruiter", "opportunity", "status"]

def clean_text(text):
    return " ".join(text.strip().split())

def extract_emails(days_back=30, max_results=100):
    messages_data = []

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select("inbox")

    # Fecha de búsqueda
    date = (datetime.date.today() - datetime.timedelta(days=days_back)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE "{date}")')

    if status != "OK":
        print("Error al buscar correos.")
        return []

    email_ids = messages[0].split()
    print(f"Se encontraron {len(email_ids)} correos desde {date}")

    for i in reversed(email_ids[-max_results:]):
        res, msg = mail.fetch(i, "(RFC822)")
        if res != "OK":
            continue

        for response_part in msg:
            if isinstance(response_part, tuple):
                msg_email = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg_email["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                from_ = msg_email.get("From")
                date_ = msg_email.get("Date")


                body = ""
                snippet = ""

                # Extraer contenido
                try:
                    if msg_email.is_multipart():
                        for part in msg_email.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True)
                                break
                            elif content_type == "text/html" and "attachment" not in content_disposition:
                                html = part.get_payload(decode=True)
                                soup = BeautifulSoup(html, "html.parser")
                                body = soup.get_text()
                                break
                    else:
                        body = msg_email.get_payload(decode=True)

                    if isinstance(body, bytes):
                        body = body.decode("utf-8", errors="ignore")

                    snippet = clean_text(body)[:500] if body else ""
                except Exception:
                    snippet = ""

                # Filtro por palabras clave
                if any(k.lower() in subject.lower() or k.lower() in snippet.lower() for k in KEYWORDS):
                    messages_data.append({
                        "from": from_,
                        "subject": subject,
                        "date": date_,
                        "snippet": snippet
                    })

    mail.logout()
    return messages_data

def extract_all_emails(days_back=90, max_results=1000):
    messages_data = []

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select("inbox")

    date = (datetime.date.today() - datetime.timedelta(days=days_back)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE "{date}")')

    if status != "OK":
        print("Error al buscar correos.")
        return []

    email_ids = messages[0].split()
    print(f"📬 Correos encontrados desde {date}: {len(email_ids)}")

    for i in reversed(email_ids[-max_results:]):
        res, msg = mail.fetch(i, "(RFC822)")
        if res != "OK":
            continue

        for response_part in msg:
            if isinstance(response_part, tuple):
                msg_email = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg_email["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                from_ = msg_email.get("From")
                date_ = msg_email.get("Date")

                # Intentar extraer fragmento de cuerpo como ref
                snippet = ""
                try:
                    if msg_email.is_multipart():
                        for part in msg_email.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                if isinstance(body, bytes):
                                    body = body.decode("utf-8", errors="ignore")
                                snippet = clean_text(body)[:300]
                                break
                    else:
                        body = msg_email.get_payload(decode=True)
                        if isinstance(body, bytes):
                            body = body.decode("utf-8", errors="ignore")
                        snippet = clean_text(body)[:300]
                except:
                    pass

                messages_data.append({
                    "from": from_,
                    "subject": subject,
                    "date": date_,
                    "snippet": snippet
                })

    mail.logout()
    return messages_data



# Prueba rápida
if __name__ == "__main__":
    emails = extract_emails()
    for e in emails:
        print(f"\n🟩 {e['date']} | {e['from']}\nAsunto: {e['subject']}\n---\n{e['snippet'][:200]}\n")