# Importamos las herramientas necesarias
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from models import AlcoholLogisticModel
import os

def ejecutar_test():
    print("--- INICIANDO TEST DE LA CLASE AlcoholLogisticModel ---")

    #Crear datos inventados
    print("\n1. Generando datos falsos para la prueba...")
    X_dummy, y_dummy = make_classification(n_samples=1000, n_features=5, n_classes=2, weights=[0.9, 0.1], random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X_dummy, y_dummy, test_size=0.2, random_state=42)
    print("Datos generados correctamente.")

    print("\n2. Creando el modelo (instanciando la clase)...")
    modelo_test = AlcoholLogisticModel(max_iter=100)

    print("\n3. Probando la función fit()...")
    modelo_test.fit(X_train, y_train)

    print("\n4. Probando la función evaluate()...")
    metricas = modelo_test.evaluate(X_test, y_test)
    claves = {'accuracy', 'precision', 'recall', 'f1', 'confusion_matrix'}
    assert claves == set(metricas), f"Faltan metricas: {claves - set(metricas)}"
    assert metricas['confusion_matrix'].shape == (2, 2)
    print("Metricas devueltas:", {k: round(v, 3) for k, v in metricas.items() if k != 'confusion_matrix'})

    print("\n5. Probando guardar y cargar en disco...")
    archivo_test = "modelo_prueba_temporal.pkl"
    modelo_test.save_model(archivo_test)
    
    modelo_clon = AlcoholLogisticModel() # probamos la lectura de ficheros externos
    modelo_clon.load_model(archivo_test)

    # El modelo cargado debe dar exactamente las mismas predicciones que el original
    assert np.array_equal(modelo_test.predict(X_test), modelo_clon.predict(X_test)), "El modelo cargado predice distinto al original"
    print("El modelo cargado produce las mismas predicciones que el original.")

    if os.path.exists(archivo_test):
        os.remove(archivo_test)
        print("Archivo temporal de prueba borrado con éxito.")

    print("\nTest finalizado correctamente")