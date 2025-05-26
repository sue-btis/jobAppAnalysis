# keyword_analysis.py

import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    text = re.sub(r"http\S+|www\S+", "", text)  # URLs
    text = re.sub(r"[^\w\s]", "", text)         # Puntuación
    text = re.sub(r"\d+", "", text)             # Números
    return text.lower()

def analizar_palabras_frecuentes(file="tracker.csv", top_n=30):
    df = pd.read_csv(file)
    all_text = " ".join(df["subject"].fillna("") + " " + df["snippet"].fillna(""))
    clean = clean_text(all_text)

    tokens = word_tokenize(clean)
    palabras_filtradas = [
        word for word in tokens if word not in stopwords.words("english") and len(word) > 2
    ]

    frecuencia = Counter(palabras_filtradas)
    top = frecuencia.most_common(top_n)

    print(f"\n🔝 Top {top_n} palabras más frecuentes en tus correos:")
    for palabra, cuenta in top:
        print(f"{palabra:>15}: {cuenta}")

if __name__ == "__main__":
    analizar_palabras_frecuentes()
