import imaplib, email, datetime
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


load_dotenv()

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
APP_PASSWORD = os.getenv("APP_PASSWORD")

EXCLUDE_SENDERS = [
    "shein", "underarmour", "price travel", "paypal", "samsung", "telmex",
    "mercadolibre", "soriana", "uber", "didi", "dominos", "netflix", "banorte",
    "banamex", "hsbc", "bbva", "newsletters", "marketing", "promocion", "dick´s",
    "leetcode", "e.dcsg", "adidas", "coursera", "tokioschool", "kaggle",
    "alerta de empleo", "we thought this job", "new job opportunities", "glassdoor",
    "crew@hyperskill.org", "epam", "donotreply@match.indeed.com", "support@jobgether.com",
    "ota@career.oracle.com", "noreply@glassdoor.com", "consubanco",
    "recruitingnoreply@ford.com", "alert@indeed.com","noreply@hola.hey.inc","mailer@knowely.com",
    "marcelo@4geeksacademy.com","messages-noreply@linkedin.com","noreply@github.com","noreply@hola.hey.inc",
    "noreply@rebrandly.com","notifications-noreply@linkedin.com","talent@itj.com","applications@bairesdev.com",
]

def clean_text(text):
    return " ".join(text.strip().split())

def extract_emails(days_back=90, max_results=1000):
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

                raw_from = msg_email.get("From") or ""
                name, email_addr = parseaddr(raw_from)
                name = name.lower()
                email_addr = email_addr.lower()

                # Filtro de remitentes excluidos (por nombre o dirección de correo)
                if any(excl in name or excl in email_addr for excl in EXCLUDE_SENDERS):
                    continue

                date_ = msg_email.get("Date") or ""
                body = ""
                snippet = ""

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

                messages_data.append({
                    "from": raw_from,
                    "subject": subject,
                    "date": date_,
                    "snippet": snippet
                })

    mail.logout()
    return messages_data
