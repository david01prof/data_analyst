# 🍽️ Predicción de GRADE en Inspecciones de Restaurantes de NYC (XGBoost)

## 🎯 Objetivo

Clasificar de forma binaria si un restaurante inspeccionado por el DOHMH (Departamento de
Salud de Nueva York) obtiene calificación **A** (buen desempeño) frente a **B/C** (desempeño
deficiente), a partir de las variables recogidas en cada inspección.

## 📦 Dataset

| Archivo | Contenido |
|---|---|
| `data/DOHMH_New_York_City_Restaurant_Inspection_Results_20260820.csv` | Dataset principal — 295.473 filas × 27 columnas (una fila por violación/inspección). **No está en el repositorio** (~152 MB): descárgalo de [NYC Open Data](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) y colócalo en `data/` |
| `data/RestaurantInspectionDataDictionary_09242018.xlsx` | Diccionario oficial de columnas (significado de cada campo, códigos de BORO, valores de GRADE/CRITICAL FLAG, etc.) |
| `doc/About_NYC_Restaurant_Inspection_Data_on_NYC_OpenData_050222.docx` | Notas de uso oficiales de NYC OpenData: explica el proceso de adjudicación, qué inspecciones son "gradables" y cómo se asigna el GRADE |

## 🧭 Pipeline (`index.ipynb`)

| Fase | Contenido |
|---|---|
| **1. Exploración inicial** | `columns`, `shape` (295.473 × 27), `dtypes` |
| **2. Limpieza** | Nulos de `GRADE` → `'unclassified'`; recast de identificadores geográficos (`ZIPCODE`, `BIN`, `BBL`, `Community Board`, `Council District`) a `object` para que no se traten como numéricos; parseo de fechas y extracción de año/mes |
| **3. Investigación de nulos en SCORE** | Cruce `GRADE=unclassified` vs `SCORE` nulo → se descarta la hipótesis de que la falta de GRADE se deba a falta de evaluación |
| **4. Preparación del target** | Filtro a `GRADE ∈ {A, B, C}` (129.339 registros); target binario `A=1`, `B/C=0`; limpieza de `Latitude`/`Longitude`; matriz de correlación con el target |
| **5. Feature engineering** | Top 10 `VIOLATION CODE` → columnas binarias `VIOL_*`; nº total de violaciones por restaurante; One-Hot de `BORO` y `CRITICAL FLAG`; `CUISINE DESCRIPTION` agrupada en top 15 + `OTHER` |
| **6. Selección de features** | 36 features finales, **excluyendo `SCORE` e `INSPECTION TYPE` por fuga de datos** (ver abajo); eliminación de 991 filas con nulos residuales (128.348 filas, 24.759 restaurantes) |
| **7. Modelado** | `XGBClassifier` + `GroupKFold` (5 folds, agrupado por `CAMIS` para que un mismo restaurante no esté a la vez en train y test) |
| **8. Feature importance** | Importancia por ganancia (`gain`) de cada variable |
| **9. Evaluación final** | Hold-out 80/20 con `GroupShuffleSplit` |

## 📊 Resultados

**Cross-validation (5 folds, agrupado por restaurante):**

| Métrica | Media | Std |
|---|---|---|
| ROC-AUC | 0.829 | 0.005 |
| F1 | 0.842 | 0.001 |
| Precision | 0.891 | 0.002 |
| Recall | 0.798 | 0.002 |

**Hold-out (20 %, 25.448 filas):** ROC-AUC 0.831 · F1 0.847 · Precision 0.894 · Recall 0.805 · Accuracy 0.78

| Clase | Precision | Recall | F1 |
|---|---|---|---|
| B/C (0) | 0.52 | 0.69 | 0.60 |
| A (1) | 0.89 | 0.80 | 0.85 |

El modelo detecta bien la clase A, y para B/C (el 24 % de los casos, que es la que más interesa al regulador) acierta el 69 % de las veces pero con una precisión baja (0.52).

**Variables más importantes (ganancia):** `VIOL_10F`, `VIOL_08A`, `num_violaciones`, `CRITICAL FLAG_Not Critical`, `VIOL_06D`, más algunos tipos de cocina (donuts, hamburguesas, café/té).

## ⚠️ Fuga de datos detectada y corregida

La primera versión del modelo daba un ROC-AUC de ≈ 0.9998, un resultado demasiado bueno para ser cierto. La causa era una **fuga de información (data leakage)**:

1. **`GRADE` es una función determinista de `SCORE`**, fijada por la normativa del programa de
   calificación de NYC (documentada en el `.docx` oficial adjunto):
   - `SCORE` 0–13 → Grade **A**
   - `SCORE` 14–27 → Grade **B**
   - `SCORE` ≥ 28 → Grade **C**

   Con `SCORE` como feature, el modelo no predice nada: reconstruye una regla aritmética conocida. La
   correlación `SCORE`–`target` (**-0.775**, la más alta con diferencia) ya lo anticipaba.
2. **`INSPECTION TYPE`** (la variable más importante de esa primera versión) identifica la inspección que
   genera la nota, por lo que actúa como proxy del resultado.

**Corrección:** ambas variables se excluyen del modelo, que pasa a usar solo información de la
inspección que no determina el resultado (infracciones, tipo de cocina, ubicación, mes). Con eso el
ROC-AUC baja a ≈ 0.83, que es el rendimiento real del problema.

**Limitación pendiente:** el modelo sigue usando información de la propia inspección (las violaciones
registradas en ella). Para *anticipar* qué restaurantes tienen riesgo de sacar mala nota **antes**
de ser inspeccionados, habría que usar solo el histórico de inspecciones previas, la cocina, la
ubicación, la antigüedad, etc.

## 🛠️ Cómo ejecutar

```bash
pip install -r requirements.txt
# descarga el CSV a data/ (ver tabla del Dataset)
jupyter notebook index.ipynb
```

## 📁 Archivos de este módulo

```text
02_CLASIFICACION_NYC_RESTAURANTS/
├── index.ipynb          # Notebook con el pipeline completo
├── data/
│   └── RestaurantInspectionDataDictionary_09242018.xlsx   # Diccionario de columnas (el CSV se descarga aparte)
├── doc/
│   └── About_NYC_Restaurant_Inspection_Data_on_NYC_OpenData_050222.docx
├── requirements.txt
└── README.md
```
