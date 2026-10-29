import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

class AlcoholLogisticModel:
    def __init__(self, random_state=42, class_weight='balanced', **kwargs):
        self.model = LogisticRegression(random_state=random_state, class_weight=class_weight, **kwargs) # usamos balanced, para que el modelo preste mas atencion
        self.is_trained = False
        
    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Modelo entrenado correctamente")
        
    def predict(self, X_test):
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado con fit() antes de predecir")
        return self.model.predict(X_test)
        
    def evaluate(self, X_test, y_test):
        """Devuelve un diccionario con las metricas de evaluacion.

        Con clases desbalanceadas la exactitud sola es engañosa, por eso se
        incluyen tambien precision, recall, F1 y la matriz de confusion.
        """
        y_pred = self.predict(X_test)

        metricas = {
            'accuracy': accuracy_score(y_test, y_pred), # comparo precision de aciertos del examen
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
        }

        print("Modelo evaluado")

        return metricas
        
    def save_model(self, filepath):
        """Guarda el modelo entrenado en disco."""
        if not self.is_trained:
            raise ValueError("No se puede guardar un modelo sin entrenar")
        joblib.dump(self.model, filepath)
        print(f"Modelo guardado en: {filepath}")
        
    def load_model(self, filepath):
        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"Modelo cargado desde: {filepath}")