from pydantic import BaseModel
from typing import Dict, Optional

# Schema for serving the detailed size chart
class DetailedSizeChartResponse(BaseModel):
    gender: str
    body_shape: int
    cluster_data: Dict[int, Dict[str, Dict[str, float]]]  # Cluster -> Property -> Size -> Confidence

# Schema for user feedback
class FeedbackRequest(BaseModel):
    gender: str
    body_shape: int
    cluster_label: int
    property_name: str
    original_size: str
    new_size: str
    learning_rate: Optional[float] = 0.1

# Schema for generic size chart response
class GenericSizeChartResponse(BaseModel):
    size_chart: Dict[str, Dict[str, float]]  # Size -> Metric -> Value

# Schema for analytics data
class AnalyticsResponse(BaseModel):
    clusters: Dict[int, Dict[str, float]]  # Cluster -> Metric -> Value
