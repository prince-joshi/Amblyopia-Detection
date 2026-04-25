# Amblyopia Detection System

A Machine Learning project that predicts whether a child is Amblyopic (Lazy Eye) based on clinical features like Visual Acuity, Refractive Error, and Strabismus.

---

## About the Project

Amblyopia (Lazy Eye) is a vision disorder where one eye is weaker than the other. Early detection is critical for effective treatment. This project builds a binary classification model using Random Forest to detect Amblyopia in children aged 2-10 years. The model is deployed as an interactive Streamlit web application with a medical-themed UI.

---

## Dataset

- **File:** `amblyopia_detection_balanced.csv`
- **Records:** 588 patients (perfectly balanced — 294 Amblyopic, 294 Not Amblyopic)
- **Features:**
  - Age, Visual Acuity (Left & Right Eye)
  - Refractive Error, Ocular Alignment
  - Strabismus, Family History
  - Premature Birth, Eye Patching Treatment
  - Vision Screening Result
- **Target:** `Amblyopic` (Yes / No)

> **Note:** Amblyopia-specific clinical CSV datasets are not publicly available due to medical data privacy. This dataset was synthetically generated based on clinically relevant features used in real ophthalmology practice.

---

## Workflow

1. Loaded and explored the dataset
2. Performed EDA — class distribution, Strabismus vs Amblyopic, Family History vs Amblyopic, Ocular Alignment vs Amblyopic
3. Dropped Patient_ID (irrelevant for prediction)
4. Applied Label Encoding to convert categorical columns to numbers
5. Split data into 80% train and 20% test
6. Trained and compared two models — Decision Tree and Random Forest
7. Evaluated using Accuracy, Classification Report, Confusion Matrix, and Feature Importance
8. Saved the best model using joblib
9. Built an interactive Streamlit web app for real-time prediction

---

## Tech Stack

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- Streamlit
- Joblib

---

## Results

| Model | Accuracy |
|-------|----------|
| Decision Tree | 84% |
| **Random Forest (Final Model)** | **91%** |

**Random Forest outperformed Decision Tree and was selected as the final model.**

---

## Streamlit App Features

- Sidebar with patient input fields and tooltips
- Model confidence score with progress bar
- Risk level indicator (Low / Medium / High)
- Patient summary card after prediction
- About Amblyopia section — Symptoms, Causes, Treatment
- Model performance metrics — Accuracy, Records, Trees, Features


---

## Files

| File | Description |
|------|-------------|
| `amblyopia_detection.ipynb` | Main notebook — EDA, preprocessing, model training, evaluation |
| `amblyopia_detection_balanced.csv` | Balanced dataset — 588 patient records |
| `amblyopia_rf_model.pkl` | Saved Random Forest model |
| `amblyopia_app.py` | Streamlit web app for real-time prediction |

---

*Developed by Prince Joshi | Aspiring Data Analyst*
