from collections import Counter
import re

try:
    import nltk
    nltk.download('punkt', quiet=True)
    from nltk.tokenize import word_tokenize, sent_tokenize
    USE_NLTK = True
except ImportError:
    USE_NLTK = False

def simple_tokenize(text):
    return re.findall(r'\w+', text.lower())

def simple_sentence_tokenize(text):
    return re.split(r'[.!?]+', text)

def analyze_text(text):
    if USE_NLTK:
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
    else:
        words = simple_tokenize(text)
        sentences = simple_sentence_tokenize(text)
    
    word_freq = Counter(words)
    
    non_empty_sentences = [s.strip() for s in sentences if s.strip()]
    avg_sentence_length = sum(len(simple_tokenize(sentence)) for sentence in non_empty_sentences) / len(non_empty_sentences) if non_empty_sentences else 0
    
    content_words = [word for word in words if len(word) > 3]
    most_common_words = Counter(content_words).most_common(5)
    
    return {
        "word_frequency": dict(word_freq),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "most_common_words": most_common_words,
        "total_words": len(words),
        "total_sentences": len(non_empty_sentences)
    }

def process_message(message):
    return analyze_text(message)

# Example usage
if __name__ == "__main__":
    sample_text = "This is a sample sentence. This is another sentence! Is this working? Yes, it is."
    result = process_message(sample_text)
    print(result)