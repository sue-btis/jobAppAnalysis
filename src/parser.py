def classify_status(subject,snippet):
    text = f"{subject} {snippet}".lower()

    if any(p in text for p in ["interview", "schedule", "invite", "calendly"]):
        return "Entrevista"
    elif any(p in text for p in ["offer", "congratulations", "hired"]):
        return "Oferta"
    elif any(p in text for p in ["rejected", "unfortunately", "not selected", "decline"]):
        return "Rechazo"
    elif any(p in text for p in ["application received", "thank you for applying", "submission"]):
        return "Aplicación recibida"
    else:
        return "Otro"

def process_mail_List(correos):
    for c in correos:
        c["estado"] = classify_status(c["subject"], c["snippet"])
    return correos