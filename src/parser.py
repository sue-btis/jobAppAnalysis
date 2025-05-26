import re

def classify_status(subject, snippet):
    text = f"{subject} {snippet}".lower()

    if any(p in text for p in ["interview", "schedule", "invite", "calendly","entrevista","agendar"]):
        return "Entrevista"
    elif any(p in text for p in ["offer", "congratulations", "hired","contratado"]):
        return "Oferta"
    elif any(p in text for p in ["rejected", "unfortunately", "not selected", "decline","canceled","rechazado","lamentablemente","desafortunadamente"]):
        return "Rechazo"
    elif any(p in text for p in ["application received", "thank you for applying", "submission"]):
        return "Aplicación recibida"
    else:
        return "Otro"

def is_relevant(subject, snippet):
    STRICT_APPLICATION_TERMS = [
        r"\bpostulación\b", r"\bpostulacion\b", r"\bapplication\b",
        r"\bthank you for applying\b", r"\bgracias por tu aplicación\b", r"\bgracias por tu aplicacion\b",
        r"\bcandidatura\b", r"\bvacante\b", r"\bposición\b", r"\bposicion\b", r"\bsolicitud\b", r"\baplicar\b",

        # Confirmación de pasos posteriores
        r"\binterview\b", r"\bentrevista\b", r"\bcalendly\b", r"\bschedule\b", r"\binvitation\b",
        r"\boffer\b", r"\bcongratulations\b", r"\bhired\b",
        r"\brejected\b", r"\bunfortunately\b", r"\bnot selected\b", r"\bdecline\b",r"\bcanceled\b"
    ]

    text = f"{subject} {snippet}".lower()
    return any(re.search(pattern, text) for pattern in STRICT_APPLICATION_TERMS)

def process_mail_List(correos):
    for c in correos:
        c["estado"] = classify_status(c["subject"], c["snippet"])
        c["relevante"] = is_relevant(c["subject"], c["snippet"])
    return correos


