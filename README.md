# 🚀 Data Analysis & Big Data Portfolio

Repositorio de proyectos desarrollados en el marco del **Máster en Data Analysis, IA y Big Data**.
Reúne análisis exploratorios de datos (EDA) y modelos de Machine Learning orientados a resolver
problemas de negocio mediante el uso de datos a escala.

---

## 🛠️ Tecnologías y Herramientas

**Big Data & Procesamiento**
- Apache Spark (PySpark, PySpark SQL)
- Pandas, NumPy

**Machine Learning & Analítica**
- Scikit-Learn, XGBoost, Spark MLlib
- Regresión (lineal/logística), clasificación (XGBoost + K-Fold Cross Validation)

**Visualización**
- Seaborn, Matplotlib

**Entorno & Infraestructura**
- Python 3.x, SQL
- Git & GitHub

---

## 📚 Proyectos

| Proyecto | Descripción | Tecnologías clave |
| :--- | :--- | :--- |
| [`01_PROCESAMIENTO_Y_EDA/`](./01_PROCESAMIENTO_Y_EDA) | Análisis exploratorio de datos, tratamiento de nulos y *feature engineering* sobre dataset de seguros médicos usando PySpark. | PySpark, Pandas, Seaborn |
| [`02_CLASIFICACION_NYC_RESTAURANTS/`](./02_CLASIFICACION_NYC_RESTAURANTS) | Clasificación binaria del GRADE (A vs B/C) de restaurantes de NYC a partir del dataset de inspecciones del DOHMH (NYC Open Data). Incluye EDA, limpieza, feature engineering y modelado con XGBoost + GroupKFold. ⚠️ Incluye advertencia documentada de data leakage (GRADE es función determinista de SCORE). | Pandas, Scikit-Learn, XGBoost, Seaborn |

> 🔜 Próximos módulos en desarrollo: pipelines ETL, modelos de clustering con Spark MLlib y un proyecto final end-to-end.

---

## 📂 Estructura del repositorio

```text
.
├── 01_PROCESAMIENTO_Y_EDA/           # Notebooks de análisis exploratorio y preprocesado con PySpark
├── 02_CLASIFICACION_NYC_RESTAURANTS/ # Clasificación de GRADE con XGBoost (dataset NYC OpenData)
├── data/                             # Datasets de muestra utilizados en los proyectos
├── .gitignore
└── README.md
```

---

## ⚙️ Cómo ejecutar los notebooks

```bash
git clone https://github.com/david01prof/data_analyst.git
cd data_analyst
pip install -r requirements.txt
jupyter notebook
```

Cada módulo incluye su propio `README.md` con el detalle del pipeline, resultados y, cuando
aplica, advertencias metodológicas a tener en cuenta antes de reutilizar el modelo.
