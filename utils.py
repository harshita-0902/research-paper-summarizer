def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text

def chunk_text(text, max_chunk=500):
    words = text.split()
    return [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]