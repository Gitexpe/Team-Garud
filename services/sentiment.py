import os
import logging
from typing import List, Dict, Any
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

logger = logging.getLogger(__name__)

class SentimentService:
    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

    def load_pipeline(self, model_name: str = "distilbert-base-uncased-fine-tuned-sst-2-english"):
        """
        Load the sentiment analysis pipeline
        """
        try:
            if not self.pipeline:
                logger.info(f"Loading sentiment analysis model: {model_name}")
                self.pipeline = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    device=self.device
                )
                logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def analyze_sentiment(
        self,
        text: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of a text
        Returns sentiment label and score
        """
        try:
            if not self.pipeline:
                self.load_pipeline()

            # Process the text
            result = self.pipeline(text)[0]
            
            return {
                "sentiment": result["label"].lower(),
                "confidence": result["score"]
            }

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            raise

    def analyze_segments(
        self,
        segments: List[Dict[str, Any]],
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for a list of segments
        """
        try:
            for segment in segments:
                if segment["text"]:  # Only analyze if there's text
                    sentiment_result = self.analyze_sentiment(
                        segment["text"],
                        language
                    )
                    segment["sentiment"] = sentiment_result["sentiment"]
                    segment["confidence"] = sentiment_result["confidence"]
                else:
                    segment["sentiment"] = "neutral"
                    segment["confidence"] = 0.0

            return segments

        except Exception as e:
            logger.error(f"Error analyzing segments: {str(e)}")
            raise

    def get_sentiment_summary(
        self,
        segments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a summary of sentiment analysis
        """
        try:
            sentiment_counts = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
            
            total_confidence = 0.0
            count = 0

            for segment in segments:
                if segment.get("sentiment"):
                    sentiment = segment["sentiment"].lower()
                    if sentiment in sentiment_counts:
                        sentiment_counts[sentiment] += 1
                        total_confidence += segment.get("confidence", 0.0)
                        count += 1

            average_confidence = total_confidence / count if count > 0 else 0.0

            return {
                "sentiment_distribution": sentiment_counts,
                "average_confidence": average_confidence,
                "total_segments": count
            }

        except Exception as e:
            logger.error(f"Error generating sentiment summary: {str(e)}")
            raise

# Create a singleton instance
sentiment_service = SentimentService()

# Export functions for use in tasks
def analyze_sentiment(text: str, language: str = "en") -> Dict[str, Any]:
    return sentiment_service.analyze_sentiment(text, language)

def analyze_segments(segments: List[Dict[str, Any]], language: str = "en") -> List[Dict[str, Any]]:
    return sentiment_service.analyze_segments(segments, language)

def get_sentiment_summary(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    return sentiment_service.get_sentiment_summary(segments) 