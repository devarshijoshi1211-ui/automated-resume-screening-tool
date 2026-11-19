import re

def clean_text(text: str) -> str:
    """Normalize text while retaining useful technical punctuation."""
    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[\r\t]+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
