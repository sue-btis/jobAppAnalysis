import re

def classify_status(subject, snippet):
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

def is_relevant(subject, snippet):
    REGEX_KEYWORDS = [
        # Roles y cargos
        r"\bdata analyst\b", r"\banalista de datos\b",
        r"\bdata scientist\b", r"\bcientifico de datos\b", r"\bcientífico de datos\b",
        r"\bjunior analyst\b", r"\banalista junior\b",
        r"\bpower bi\b", r"\bingeniero de datos\b",
        r"\bbackend developer\b", r"\bfrontend developer\b", r"\bfull stack\b",
        r"\bqa engineer\b", r"\bqa\b",
        r"\bdesarrollador\b", r"\bprogramador\b", r"\bsoftware engineer\b", r"\bconsultor\b",

        # Internships
        r"\bintern\b", r"\binternship\b", r"\bbecario\b", r"\btrainee\b", r"\bintern it\b",

        # Proceso de selección / Aplicación
        r"\bpostulación\b", r"\bpostulacion\b", r"\bapplication\b",
        r"\bthank you for applying\b", r"\bgracias por tu aplicación\b", r"\bgracias por tu aplicacion\b",
        r"\bcandidatura\b", r"\bvacante\b", r"\bposición\b", r"\bposicion\b",
        r"\bjob opportunity\b", r"\bnew job\b", r"\bapply\b", r"\bsolicitud\b", r"\baplicar\b",
        r"\bwe are hiring\b", r"\bwe're hiring\b", r"\bjoin our team\b",

        # Reclutadores y entrevistas
        r"\brecruiter\b", r"\bhiring\b", r"\brecruitment\b",
        r"\bentrevista\b", r"\binterview\b", r"\bcalendly\b",

        # Skills y herramientas
        r"\bsql\b", r"\bpython\b", r"\br\b", r"\bjava\b", r"\bjavascript\b",
        r"\bexcel\b", r"\bdashboard\b", r"\betl\b", r"\btableau\b", r"\bpower bi\b",
        r"\bmachine learning\b", r"\baws\b", r"\bazure\b",

        # Modalidades y contexto
        r"\bremote\b", r"\bremoto\b", r"\bhybrid\b", r"\bhíbrido\b",
        r"\bcareer\b", r"\bcarrera\b", r"\bcv\b", r"\bcurriculum\b", r"\bcurrículum\b",

        # Oportunidades
        r"\bopen position\b", r"\bnow hiring\b", r"\bcareer opportunity\b", r"\bnueva oportunidad\b"
    ]

    text = f"{subject} {snippet}".lower()
    return any(re.search(pattern, text) for pattern in REGEX_KEYWORDS)

def process_mail_List(correos):
    for c in correos:
        c["estado"] = classify_status(c["subject"], c["snippet"])
        c["relevante"] = is_relevant(c["subject"], c["snippet"])
    return correos


