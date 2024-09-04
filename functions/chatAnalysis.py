from collections import Counter
import re

def analyze_chat(text):
    # Clean and tokenize the text
    words = re.findall(r'\w+', text.lower())
    
    # Count words
    word_count = len(words)
    
    # Get word frequency
    word_frequency = Counter(words)
    
    # Simple sentiment analysis
    positive_words = set(['happy', 'good', 'great', 'excellent', 'wonderful', 'fun', 'mutlu', 'iyi', 'harika', 'mükemmel', 'eğlenceli'])
    negative_words = set(['sad', 'bad', 'awful', 'terrible', 'boring', 'üzgün', 'kötü', 'berbat', 'korkunç', 'sıkıcı'])
    
    sentiment_score = sum(1 for word in words if word in positive_words) - sum(1 for word in words if word in negative_words)
    
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "word_count": word_count,
        "word_frequency": dict(word_frequency.most_common(5)),
        "sentiment": sentiment
    }