import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analytics.analytics_engine import AnalyticsEngine

# Global singleton engine instance
engine_instance = None

def get_analytics_engine() -> AnalyticsEngine:
    global engine_instance
    if engine_instance is None:
        engine_instance = AnalyticsEngine()
    return engine_instance
