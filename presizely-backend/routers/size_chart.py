from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from services.size_chart_service import results, generate_generic_size_chart
import numpy as np
from pydantic import BaseModel
import json
router = APIRouter()

# Function to convert height from "feet'inches" to centimeters
def convert_height_to_cm(height):
        try:
            feet, inches = map(int, height.replace('"', '').split("'"))
            return round(feet * 30.48 + inches * 2.54, 2)
        except:
            return None


@router.post("/generate-generic-size-chart")
def generate_generic_chart_route(num_sizes: int = Query(5, ge=1, le=10)):
    """
    Generate a generic size chart with a specified number of sizes.
    """
    try:
        chart = generate_generic_size_chart(results, num_sizes=num_sizes)
        return chart.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


@router.get("/getalldetailedcharts")
def get_all_detailed_charts():
    # Initialize an empty list to store detailed chart data
    detailed_charts = []

    # Iterate over all (gender, body_shape) combinations in the results
    for (gender, body_shape), data in results.items():
        # Extract the k-means model, subset of data, and confidence information
        kmeans = data['kmeans']
        subset = data['subset']
        size_mapping = data['size_mapping']
        cluster_confidences = data['cluster_confidences']

        # For each cluster, get the cluster details, including the centroid and size mapping
        for cluster_id in range(kmeans.n_clusters):
            # Get the centroid of the cluster
            centroid = kmeans.cluster_centers_[cluster_id]
            
            # Get the size label based on the cluster
            size_label = size_mapping.get(cluster_id, "Unknown")
            
            # Get a subset of data for this particular cluster
            cluster_data = subset[subset['Cluster'] == cluster_id]

            # Prepare detailed chart data
            chart_data = {
                'gender': gender,
                'body_shape': body_shape,
                'cluster_id': cluster_id,
                'size_label': size_label,
                'centroid': centroid.tolist(),  # Convert centroid array to list for JSON compatibility
                'cluster_count': len(cluster_data),
                'sample_data': cluster_data[['Height_cm', 'Weight', 'Bust/Chest', 'Waist', 'Hips']].head(5).to_dict(orient='records'),  # Sample data for preview
                'confidence_scores': cluster_confidences[cluster_id]
            }
            detailed_charts.append(chart_data)
    
    # Return the detailed charts as JSON
    return json.dumps(detailed_charts,cls=NpEncoder)




class UpdateSizeChartRequest(BaseModel):
    gender: str
    body_shape: int
    cluster_label: int
    property_name: str
    original_size: str
    new_size: str
    learning_rate: float = 0.1


@router.post("/update_size_chart")
def update_size_chart(data: UpdateSizeChartRequest):
    """
    Update the size chart confidence scores based on user feedback.
    """
    gender = data.gender.lower()
    body_shape = data.body_shape
    cluster_label = data.cluster_label
    property_name = data.property_name
    original_size = data.original_size.upper()
    new_size = data.new_size.upper()
    learning_rate = data.learning_rate

    # Validate the provided gender and body shape
    key = (gender, body_shape)
    if key not in results:
        raise HTTPException(status_code=404, detail="Data not available for this gender and body shape index.")

    cluster_confidences = results[key]['cluster_confidences']
    if cluster_label not in cluster_confidences:
        raise HTTPException(status_code=404, detail="Invalid cluster label.")

    # Validate the property
    confidence_scores = cluster_confidences[cluster_label].get(property_name, None)
    if confidence_scores is None:
        raise HTTPException(status_code=404, detail="Invalid property name.")

    if original_size not in confidence_scores or new_size not in confidence_scores:
        raise HTTPException(status_code=400, detail="Invalid size value provided.")

    # Adjust the confidence scores for the specified property
    confidence_scores[original_size] = max(0, confidence_scores[original_size] - learning_rate)
    confidence_scores[new_size] = min(1, confidence_scores[new_size] + learning_rate)

    # Normalize confidence scores to ensure they sum to 1
    total = sum(confidence_scores.values())
    for size in confidence_scores:
        confidence_scores[size] /= total

    # Return the updated confidence scores
    return {
        "message": "Confidence scores updated successfully.",
        "confidence_scores": confidence_scores
    }

class PredictSizeRequest(BaseModel):
    gender: str
    body_shape: int
    height: str  # Input height as a string (e.g., "5'7")
    weight: float
    bust_chest: float
    waist: float
    hips: float

@router.post("/predict_size")
def predict_size(data: PredictSizeRequest):
    """
    Predict the recommended size based on user measurements.
    """
    print("data ",data)
    gender = data.gender.lower()
    body_shape = data.body_shape
    height = data.height
    weight = data.weight
    bust_chest = data.bust_chest
    waist = data.waist
    hips = data.hips

    # Convert height to cm
    height_cm = convert_height_to_cm(height)
    if height_cm is None:
        raise HTTPException(status_code=400, detail="Invalid height input format. Use format like 5'7.")

    # Create input feature array
    input_features = np.array([[height_cm, weight, bust_chest, waist, hips]])

    # Check if the key exists in results
    key = (gender, body_shape)
    if key not in results:
        raise HTTPException(status_code=404, detail="Data not available for this gender and body shape index.")

    kmeans = results[key]['kmeans']
    cluster_confidences = results[key]['cluster_confidences']

    if kmeans is None:
        raise HTTPException(status_code=500, detail="Clustering model not available for this gender and body shape.")

    # Predict the cluster for the input features
    cluster_label = kmeans.predict(input_features)[0]

    # Aggregate confidence scores for the predicted cluster
    confidence_scores = cluster_confidences[cluster_label]
    aggregated_scores = {'S': 0, 'M': 0, 'L': 0, 'XL': 0}
    for property_scores in confidence_scores.values():
        for size, score in property_scores.items():
            aggregated_scores[size] += score

    # Determine the size with the highest confidence
    predicted_size = max(aggregated_scores, key=aggregated_scores.get)
    return {"predicted_size": predicted_size}

