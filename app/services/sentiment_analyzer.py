from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> dict:
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_score = blob.sentiment.polarity

        # VADER analysis
        vader_scores = self.vader.polarity_scores(text)
        vader_score = vader_scores['compound']

        # Combine scores (you can adjust weights as needed)
        combined_score = (textblob_score + vader_score) / 2

        # Determine sentiment label
        if combined_score >= 0.05:
            label = "Positive"
        elif combined_score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "score": combined_score,
            "label": label,
            "details": {
                "textblob_score": textblob_score,
                "vader_score": vader_score,
                "vader_scores": vader_scores
            }
        } 