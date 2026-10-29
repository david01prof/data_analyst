# 🏥 Costes de seguros médicos con PySpark (EDA + Regresión Lineal)

## 🎯 Objetivo

Analizar y predecir el coste (`charges`) del seguro médico de cada beneficiario a partir de su edad,
sexo, IMC, nº de hijos, si fuma y su región, usando **PySpark** (pandas-on-Spark para el EDA y Spark ML para el modelado).

## 📦 Dataset

`insurance.csv` — 1.338 filas × 7 columnas (`age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`).
Fuente: [stedy/Machine-Learning-with-R-datasets](https://github.com/stedy/Machine-Learning-with-R-datasets/blob/master/insurance.csv).

## 🧭 Contenido (`pySpark.ipynb`)

| Fase | Contenido |
|---|---|
| **EDA** | Tipos, nulos, descriptivos y detección de outliers (IQR) en `charges` y `bmi` |
| **Relaciones** | Mapa de calor y gráficos de `charges` frente a edad, fumador y obesidad (interacción fumador × obeso) |
| **Preprocesado** | `StringIndexer`, `OneHotEncoder`, `VectorAssembler`, `StandardScaler`, transformación `log1p` del objetivo. El preprocesado se ajusta **solo con train** |
| **Modelado** | Regresión lineal de Spark ML; ajuste de hiperparámetros con **Hyperopt** (validación dentro de train) y `CrossValidator` (3 folds, solo sobre train) |
| **Comparación** | Cinco modelos con métricas en USD (R², RMSE y MAE) en train y test |

## 📊 Resultados (test)

| Modelo | R² | RMSE | MAE |
|---|---|---|---|
| 1. Lineal sobre `charges` | 0.796 | 5,661 $ | 3,960 $ |
| 2. Lineal sobre `log_charges` | 0.626 | 7,653 $ | 3,652 $ |
| 3. Log + CV | 0.636 | 7,555 $ | 3,612 $ |
| 4. Log + CV + interacción | 0.389 | 9,786 $ | 4,299 $ |
| **5. Lineal + CV + interacción fumador × obeso (sin log)** | **0.895** | **4,048 $** | **2,305 $** |

**Hallazgos:**

- El coste lo determina sobre todo fumar y la obesidad **combinados**: un fumador obeso cuesta de media ≈ 42 k$ frente a ≈ 21 k$ del fumador no obeso.
- La interacción fumador × obeso es lo que más mejora el modelo, pero **solo si el objetivo se deja en dólares**. Con `log1p(charges)` el efecto se vuelve multiplicativo, el modelo sobreestima a los fumadores obesos y el RMSE empeora (modelo 4). La transformación logarítmica tampoco mejoró el RMSE ni el R² del modelo base.
- Limitaciones: el mejor `regParam` del modelo 5 cae en el borde del grid, no se han revisado los residuos y todo se basa en una sola partición train/test.

## 🛠️ Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook pySpark.ipynb
```

Requisitos: **Java 17 o 21** (Spark 4). Con Java 23 hay que definir antes de lanzar Jupyter
`JAVA_TOOL_OPTIONS="-Djava.security.manager=allow"`. Si hay varios Pythons instalados, define también
`PYSPARK_PYTHON` y `PYSPARK_DRIVER_PYTHON` con el del entorno donde ejecutas el notebook.

## 📁 Archivos de este módulo

```text
01_PROCESAMIENTO_Y_EDA/
├── pySpark.ipynb       # Notebook con el EDA y los modelos
├── insurance.csv       # Dataset (1.338 filas)
├── requirements.txt
└── README.md
```
