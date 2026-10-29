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
| [`01_PROCESAMIENTO_Y_EDA/`](./01_PROCESAMIENTO_Y_EDA) | EDA y regresión lineal sobre costes de seguros médicos con PySpark (pandas-on-Spark y Spark ML): preprocesado sin fuga, ajuste con Hyperopt y validación cruzada, y comparación de cinco modelos (R² test 0.80 → 0.90 al modelar la interacción fumador × obeso). | PySpark, Pandas, Seaborn |
| [`02_CLASIFICACION_NYC_RESTAURANTS/`](./02_CLASIFICACION_NYC_RESTAURANTS) | Clasificación binaria del GRADE (A vs B/C) de restaurantes de NYC a partir del dataset de inspecciones del DOHMH (NYC Open Data). Incluye EDA, limpieza, feature engineering y modelado con XGBoost + GroupKFold. Documenta la fuga de datos detectada (GRADE es función determinista de SCORE) y su corrección: ROC-AUC 0.999 → 0.83 real. | Pandas, Scikit-Learn, XGBoost, Seaborn |
| [`03_ACCIDENTES_MADRID/`](./03_ACCIDENTES_MADRID) | EDA de los partes de accidentes de Madrid (2024) respetando la granularidad persona/accidente, análisis geográfico con KDE y modelo de regresión logística para predecir positivos en alcohol, con evaluación completa (precision, recall, F1) y sin fuga de datos. | Pandas, Scikit-Learn, Seaborn |

> 🔜 Próximos módulos en desarrollo: pipelines ETL, modelos de clustering con Spark MLlib y un proyecto final end-to-end.

---

## 📂 Estructura del repositorio

```text
.
├── 01_PROCESAMIENTO_Y_EDA/           # Notebooks de análisis exploratorio y preprocesado con PySpark
├── 02_CLASIFICACION_NYC_RESTAURANTS/ # Clasificación de GRADE con XGBoost (dataset NYC OpenData)
├── 03_ACCIDENTES_MADRID/             # EDA y regresión logística (alcohol) sobre accidentes de Madrid
├── .gitignore
└── README.md
```

---

## ⚙️ Cómo ejecutar los notebooks

Cada módulo tiene sus propias dependencias (`requirements.txt`) y, cuando los datos son
pesados, instrucciones para descargarlos en su `README.md`.

```bash
git clone https://github.com/david01prof/data_analyst.git
cd data_analyst/03_ACCIDENTES_MADRID     # o el módulo que quieras ejecutar
pip install -r requirements.txt
jupyter notebook
```

Cada módulo incluye su propio `README.md` con el detalle del pipeline, resultados y, cuando
aplica, advertencias metodológicas a tener en cuenta antes de reutilizar el modelo.
