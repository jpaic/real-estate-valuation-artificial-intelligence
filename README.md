# Real Estate Price Prediction Using Machine Learning

## Overview

A machine learning project for estimating real estate market prices.

The system collects real estate listing data, processes property features, and trains and compares several regression algorithms to predict property prices, in order to determine which approach performs best on this dataset.

---

## Dataset

The dataset was created by collecting real estate listings and extracting relevant property information.

Features include:

- Location (municipality, neighborhood, distance from city center)
- Area size
- Number of rooms and bathrooms
- Floor
- Elevator, balcony, terrace
- Heating type
- Other property characteristics

Target variable:

- `price_eur` (log-transformed for training)

---

## Models

The project trains and compares the following regression algorithms:

- Linear Regression
- Decision Tree
- Random Forest
- XGBoost
- CatBoost
- LightGBM
- Multi Layer Perceptron (MLP) neural network

All models use the same preprocessing pipeline, train/test split, and cross-validation folds, to ensure a fair comparison.

---

## Evaluation

Models are evaluated using:

- MAE
- RMSE
- MAPE
- R² Score

Model performance is compared through cross-validation, statistical significance testing, residual analysis, and feature importance / SHAP analysis.

---

## Technologies

- Python
- Scikit-learn
- XGBoost, LightGBM, CatBoost
- TensorFlow / Keras
- SHAP
- Pandas, NumPy
- Matplotlib, Seaborn

---

## Application

The system can support automated property valuation and real estate market analysis by providing estimated property prices based on historical listing data.
