# **Dynamic Clothing Size Prediction System**

An intelligent size prediction and optimization system for clothing that leverages clustering and user feedback to dynamically adjust sizing recommendations for improved accuracy.

---

## **Features**
- **Clustering-Based Size Prediction:** Uses K-Means clustering to group body measurements into predefined clusters and assign appropriate sizes (S, M, L, XL).
- **Feedback-Driven Size Adjustment:** Dynamically updates confidence scores for sizes based on user feedback (e.g., returns due to size mismatch).
- **Customizable Size Chart:** Generates both detailed and generic size charts from clustered data, allowing for easy scaling.
- **Flexible Inputs:** Supports height in both feet/inches and centimeters and accepts key body measurements (weight, bust/chest, waist, and hips).
- **Real-Time Updates:** Continuously improves prediction accuracy by learning from user feedback.

---

## **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<username>/dynamic-size-prediction.git
   cd dynamic-size-prediction
   ```

2. **Install Dependencies:**
   Ensure you have Python installed (>=3.8) and install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Dataset:**
   - Place your dataset (`generated_body_measurements_dataset.csv`) in the project directory.
   - Ensure it includes the following fields: `Height`, `Weight`, `Bust/Chest`, `Waist`, `Hips`, `Body Shape Index`, `Gender`.

---

## **Usage**

### **1. Predict Clothing Size**
Run the script and provide input when prompted:
```bash
python size_prediction.py
```

**Input Example:**
```plaintext
Enter gender (Male/Female): Male
Enter body shape index (e.g., 0 for Short-Small): 0
Enter height (e.g., 5'7"): 5'6"
Enter weight (kg): 57
Enter bust/chest measurement (cm): 90
Enter waist measurement (cm): 85
Enter hips measurement (cm): 90
```

**Output Example:**
```plaintext
Size Label: Medium-Small, Size Category: M
```

---

### **2. Update Confidence Scores**
Use the feedback update feature to adjust size recommendations based on user returns or complaints.

**Run the Script:**
```bash
python feedback_update.py
```

**Input Example:**
```plaintext
Enter gender (Male/Female): Male
Enter body shape index: 0
Enter height (e.g., 5'7"): 5'6"
Enter weight (kg): 57
Enter bust/chest measurement (cm): 90
Enter waist measurement (cm): 85
Enter hips measurement (cm): 90
What was the reason for return? (Height/Weight/Bust/Waist/Hips): Bust
Was the size too small or too large? (small/large): small
```

**Output Example:**
```plaintext
Confidence scores updated successfully.
```

---

## **Detailed Explanation**

### **1. Size Prediction Workflow**
- **Preprocessing:** Converts height to centimeters and normalizes inputs.
- **Clustering:** Groups body measurements using K-Means into 11 detailed clusters.
- **Mapping to Sizes:** Maps clusters to size labels (e.g., S, M, L, XL) based on median height and weight thresholds.

### **2. Feedback-Based Size Updates**
- Each size has a confidence score (ranging from 0 to 1) for properties like height, weight, bust, waist, and hips.
- User feedback adjusts these scores, and the most confident property determines the updated size for a cluster.

### **3. Confidence Score Update Logic**
- If a size is returned for being too small/large for a specific property:
  - Decrease confidence for the current size.
  - Increase confidence for the next likely size based on user feedback.

---

## **Folder Structure**
```plaintext
dynamic-size-prediction/
├── datasets/
│   └── generated_body_measurements_dataset.csv
├── scripts/
│   ├── size_prediction.py  # Main script for predicting sizes
│   ├── feedback_update.py  # Script for updating confidence scores
├── README.md               # Documentation
├── requirements.txt        # Dependencies
└── utils.py                # Helper functions (conversion, clustering, etc.)
```

---

## **Technologies Used**
- **Python:** Core programming language.
- **Pandas & NumPy:** For data preprocessing and analysis.
- **scikit-learn:** For K-Means clustering.
- **Matplotlib/Seaborn (Optional):** For visualizing clusters and confidence scores.

---

## **Future Enhancements**
- Incorporate advanced ML models (e.g., Random Forests, Neural Networks) for improved predictions.
- Add support for additional size categories (e.g., XS, XXL).
- Implement a user-friendly web interface for real-time size recommendations.
- Collect and analyze feedback for further personalization.

---

## **Contributing**
Contributions are welcome! If you’d like to improve the system or add new features:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add new feature"
   git push origin feature-name
   ```
4. Create a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Contact**
For any queries or contributions, feel free to contact:
- **Name:** Akhilesh Jyotishi
- **Email:** [akhileshjyotishi1729@gmail.com]
- **GitHub:** [github.com/AkhileshJyotishi](https://github.com/AkhileshJyotishi) 
