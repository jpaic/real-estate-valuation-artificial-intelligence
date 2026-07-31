# Real Estate Valuation Using Neural Networks

## Overview

This project presents a deep learning approach for estimating real estate market values using artificial neural networks.

The goal is to develop a regression model that learns the relationship between property characteristics and market prices, enabling automated property valuation based on historical real estate data.

---

## Objective

The objective of this project is to build and evaluate a Multi Layer Perceptron (MLP) neural network capable of predicting property prices using relevant real estate features.

---

## Dataset

The dataset contains real estate listings with information about:

- Location
- Property area
- Number of rooms
- Number of bathrooms
- Floor level
- Elevator availability
- Balcony and terrace features
- Heating type
- Additional property characteristics

Target variable:

- `price_eur` — property market value in euros

---

## Model Architecture

The project uses a Multi Layer Perceptron (MLP) neural network for regression.

Architecture:

- Input layer
- Dense layer: 64 neurons with ReLU activation
- Dropout layer: 0.2
- Dense layer: 32 neurons with ReLU activation
- Output layer: 1 neuron with Linear activation

Training configuration:

- Optimizer: Adam
- Loss function: Mean Squared Error (MSE)

---

## Data Processing

The preprocessing pipeline includes:

- Handling missing values
- Encoding categorical variables
- Feature scaling
- Train/test data splitting

---

## Evaluation

The model performance is evaluated using regression metrics:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

---

## Technologies

- Python
- TensorFlow / Keras
- Pandas
- NumPy
- Scikit-learn
- Matplotlib

---

## Practical Application

The developed system can be used as a decision-support tool for:

- Real estate agencies
- Buyers and sellers
- Property investors
- Market analysis platforms

The project demonstrates the practical application of neural networks in automated real estate valuation.
