import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
# from models.schemas import DetailedSizeChartResponse, GenericSizeChartResponse, AnalyticsResponse
# from models.schemas import FeedbackRequest
from typing import Dict
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


results = {}  
generic_size_chart = {}  
analytics_data = {}  

size_mapping = {0: 'Short-Small', 1: 'Short-Medium', 2: 'Short-Full', 3: 'Medium-Very Small', 4: 'Medium-Small',
                    5: 'Medium-Medium', 6: 'Medium-Full', 7: 'Tall-Very Small', 8: 'Tall-Small', 9: 'Tall-Medium',
                    10: 'Tall-Full'}

default_confidence = {'S': 0.25, 'M': 0.25, 'L': 0.25, 'XL': 0.25}

def convert_height_to_cm(height):
        try:
            feet, inches = map(int, height.replace('"', '').split("'"))
            return round(feet * 30.48 + inches * 2.54, 2)
        except:
            return None

def initialzeInmemoryDatabase():

    print("initializing the database...")
    file_path = 'dataset/generated_body_measurements_dataset.csv'
    data = pd.read_csv(file_path)

    data['Height_cm'] = data['Height'].apply(convert_height_to_cm)
    data['Weight'] = pd.to_numeric(data['Weight'], errors='coerce')
    data['Bust/Chest'] = pd.to_numeric(data['Bust/Chest'], errors='coerce')
    data['Waist'] = pd.to_numeric(data['Waist'], errors='coerce')
    data['Hips'] = pd.to_numeric(data['Hips'], errors='coerce')
    data['Body Shape Index'] = pd.to_numeric(data['Body Shape Index'], errors='coerce')
    data['Gender'] = data['Gender'].str.lower()  # Normalize gender column

    data = data.dropna(subset=['Height_cm', 'Weight', 'Bust/Chest', 'Waist', 'Hips', 'Body Shape Index', 'Gender'])


    for gender in data['Gender'].unique():
        for body_shape in data['Body Shape Index'].unique():
            subset = data[(data['Gender'] == gender) & (data['Body Shape Index'] == body_shape)]

            if len(subset) > 11:  
                features = subset[['Height_cm', 'Weight', 'Bust/Chest', 'Waist', 'Hips']].values

                kmeans = KMeans(n_clusters=11, random_state=42)
                subset['Cluster'] = kmeans.fit_predict(features)

                cluster_confidences = {
                    cluster: {
                        'Height': default_confidence.copy(),
                        'Weight': default_confidence.copy(),
                        'Bust/Chest': default_confidence.copy(),
                        'Waist': default_confidence.copy(),
                        'Hips': default_confidence.copy()
                    }
                    for cluster in range(11)
                }

                # Save results for this combination
                results[(gender, body_shape)] = {
                    'kmeans': kmeans, #everything
                    'subset': subset, # top 200
                    'size_mapping': size_mapping, 
                    'cluster_confidences': cluster_confidences 
                }
                # print("restake ",results)
    print("initialized the database...")

# def get_detailed_chart(gender: str, body_shape: int) -> DetailedSizeChartResponse:
#     key = (gender, body_shape)
#     if key not in results:
#         raise ValueError("Data not available for this gender and body shape index.")
#     return DetailedSizeChartResponse(gender=gender, body_shape=body_shape, cluster_data=results[key])

# def get_generic_chart() -> GenericSizeChartResponse:
#     return GenericSizeChartResponse(size_chart=generic_size_chart)

# def get_analytics_data() -> AnalyticsResponse:
#     return AnalyticsResponse(clusters=analytics_data)




def update_confidence_scores():

    """
    Interactively update the confidence scores based on user feedback.
    """
    gender = input("Enter gender (Male/Female): ").strip().lower()
    body_shape = int(input("Enter body shape index (e.g., 0 for Short-Small): ").strip())
    cluster_label = int(input("Enter the cluster label: ").strip())
    property_name = input("Enter the property causing the issue (Height/Weight/Bust/Chest/Waist/Hips): ").strip()
    original_size = input("Enter the original size assigned (S/M/L/XL): ").strip().upper()
    new_size = input("Enter the new correct size (S/M/L/XL): ").strip().upper()
    learning_rate = float(input("Enter the learning rate for the adjustment (default: 0.1): ").strip() or 0.1)

    key = (gender, body_shape)
    if key not in results:
        print("Data not available for this gender and body shape index.")
        return

    cluster_confidences = results[key]['cluster_confidences']
    if cluster_label not in cluster_confidences:
        print("Invalid cluster label.")
        return

    confidence_scores = cluster_confidences[cluster_label].get(property_name, None)
    if confidence_scores is None:
        print("Invalid property name.")
        return

    print("\n**Before Update**")
    print(f"Cluster: {cluster_label}, Property: {property_name}")
    print(f"Confidence Scores: {confidence_scores}")

    confidence_scores[original_size] = max(0, confidence_scores[original_size] - learning_rate)
    confidence_scores[new_size] = min(1, confidence_scores[new_size] + learning_rate)

    total = sum(confidence_scores.values())
    for size in confidence_scores:
        confidence_scores[size] /= total
        
    print("\n**After Update**")
    print(f"Cluster: {cluster_label}, Property: {property_name}")
    print(f"Confidence Scores: {confidence_scores}")

    print("Confidence scores updated successfully.")





def generate_generic_size_chart(results, num_sizes=5):
    """
    Generate a generic size chart by merging clusters with similar feature ranges.
    Chest/Bust, Waist, and Hips measurements are hardcoded based on the provided size chart.

    Parameters:
        results (dict): Clustering results grouped by (gender, body shape index).
        num_sizes (int): Number of generic sizes (default 5 for XS, S, M, L, XL).

    Returns:
        pd.DataFrame: Generic size chart with ranges for each size category.
    """
    size_names = ['XS', 'S', 'M', 'L', 'XL'][:num_sizes]
    measurements = {
        'XS': {'Chest/Bust': '32”-33”', 'Waist': '24”-25”', 'Hips': '34.5”-35.5”'},
        'S': {'Chest/Bust': '34”-35”', 'Waist': '26”-27”', 'Hips': '36”-37”'},
        'M': {'Chest/Bust': '36”-37”', 'Waist': '28”-29”', 'Hips': '38.5”-39.5”'},
        'L': {'Chest/Bust': '38.5”-40”', 'Waist': '30.5”-32”', 'Hips': '41”-42.5”'},
        'XL': {'Chest/Bust': '41.5”-43”', 'Waist': '33.5”-35”', 'Hips': '44”-45.5”'}
    }

    all_clusters = []

    # Extract and aggregate cluster data from `results`
    for key, value in results.items():
        gender, body_shape = key
        subset = value['subset']

        # Aggregate cluster-wise data
        for cluster_label in subset['Cluster'].unique():
            cluster_subset = subset[subset['Cluster'] == cluster_label]
            all_clusters.append({
                'Gender': gender,
                'Body Shape Index': body_shape,
                'Cluster': cluster_label,
                'Height_mean': cluster_subset['Height_cm'].mean(),
                'Weight_mean': cluster_subset['Weight'].mean(),
                'Height_min': cluster_subset['Height_cm'].min(),
                'Height_max': cluster_subset['Height_cm'].max(),
                'Weight_min': cluster_subset['Weight'].min(),
                'Weight_max': cluster_subset['Weight'].max()
            })

    # Convert to a DataFrame
    cluster_data = pd.DataFrame(all_clusters)

    # Normalize feature data for clustering
    features = ['Height_mean', 'Weight_mean']
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(cluster_data[features])

    # Apply k-means clustering to group clusters into generic sizes
    kmeans = KMeans(n_clusters=num_sizes, random_state=42)
    cluster_data['Generic Size'] = kmeans.fit_predict(normalized_data)

    # Sort clusters and assign size labels
    cluster_centroids = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    cluster_centroids['Generic Size'] = cluster_centroids.index
    cluster_centroids['Size'] = size_names

    # Map size labels to clusters
    cluster_data = cluster_data.merge(cluster_centroids[['Generic Size', 'Size']], on='Generic Size')

    # Aggregate ranges for each generic size
    generic_size_chart = []
    for size in size_names:
        size_group = cluster_data[cluster_data['Size'] == size]
        generic_size_chart.append({
            'Size': size,
            'Height Range (cm)': f"{size_group['Height_min'].min()}-{size_group['Height_max'].max()}",
            'Weight Range (kg)': f"{size_group['Weight_min'].min()}-{size_group['Weight_max'].max()}",
            'Chest/Bust': measurements[size]['Chest/Bust'],
            'Waist': measurements[size]['Waist'],
            'Hips': measurements[size]['Hips']
        })

    return pd.DataFrame(generic_size_chart)
