# Real Estate Valuation Using Neural Networks

## Overview

A deep learning project for estimating real estate market values using artificial neural networks.

The system collects real estate listing data, processes property features, and trains a neural network model to predict property prices.

---

## Dataset

The dataset was created by collecting real estate listings and extracting relevant property information.

Features include:

- Location
- Area size
- Number of rooms
- Number of bathrooms
- Floor
- Elevator
- Balcony and terrace
- Heating type
- Property characteristics

Target variable:

- `price_eur`

---

## Model

The project uses a Multi Layer Perceptron (MLP) neural network for regression.

Architecture:

- Dense layer: 64 neurons (ReLU)
- Dropout layer: 0.2
- Dense layer: 32 neurons (ReLU)
- Output layer: 1 neuron (Linear)

Training:

- Optimizer: Adam
- Loss function: Mean Squared Error (MSE)

---

## Evaluation

The model is evaluated using:

- MAE
- RMSE
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

## Application

The system can support automated property valuation and real estate market analysis by providing estimated property prices based on historical data.
