# 🍽️ Predicción de GRADE en Inspecciones de Restaurantes de NYC (XGBoost)

## 🎯 Objetivo

Clasificar de forma binaria si un restaurante inspeccionado por el DOHMH (Departamento de
Salud de Nueva York) obtiene calificación **A** (buen desempeño) frente a **B/C** (desempeño
deficiente), a partir de las variables recogidas en cada inspección.

## 📦 Dataset

| Archivo | Contenido |
|---|---|
| `DOHMH_New_York_City_Restaurant_Inspection_Results_20260820.csv` | Dataset principal — 295.473 filas × 27 columnas (una fila por violación/inspección). Fuente: [NYC Open Data](https://data.cityofnewyork.us/) |
| `RestaurantInspectionDataDictionary_09242018.xlsx` | Diccionario oficial de columnas (significado de cada campo, códigos de BORO, valores de GRADE/CRITICAL FLAG, etc.) |
| `About_NYC_Restaurant_Inspection_Data_on_NYC_OpenData_050222.docx` | Notas de uso oficiales de NYC OpenData — **lectura obligatoria** antes de analizar el dataset, porque explica el proceso de adjudicación, qué inspecciones son "gradables" y cómo se asigna el GRADE |

> ⚠️ El CSV pesa ~152 MB. No se recomienda versionarlo directamente en git (añadir a
> `.gitignore` o usar Git LFS / almacenamiento externo).

## 🧭 Pipeline (`index.ipynb`)

| Fase | Contenido |
|---|---|
| **1. Exploración inicial** | `columns`, `shape` (295.473 × 27), `dtypes` |
| **2. Limpieza** | Nulos de `GRADE` → `'unclassified'`; recast de identificadores geográficos (`ZIPCODE`, `BIN`, `BBL`, `Community Board`, `Council District`) a `object` para que no se traten como numéricos; parseo de fechas (`INSPECTION DATE`, `GRADE DATE`, `RECORD DATE`) y extracción de año/mes; eliminación de las columnas de fecha originales |
| **3. Investigación de nulos en SCORE** | Cruce `GRADE=unclassified` vs `SCORE` nulo → se descarta la hipótesis de que la falta de GRADE se deba a falta de evaluación |
| **4. Preparación del target** | Filtro a `GRADE ∈ {A, B, C}` (129.339 registros); target binario `A=1`, `B/C=0`; limpieza de `Latitude`/`Longitude`; matriz de correlación con el target |
| **5. Feature engineering** | Frecuencia de `VIOLATION CODE` (top 10 → columnas binarias `VIOL_*`); nº total de violaciones por restaurante (`num_violaciones`); One-Hot de `BORO`, `CRITICAL FLAG`, `INSPECTION TYPE`; `CUISINE DESCRIPTION` agrupada en top 15 + `OTHER` |
| **6. Selección de features** | 46 features finales, sin identificadores; eliminación de filas con nulos residuales |
| **7. Modelado** | `XGBClassifier` + `GroupKFold` (5 folds, agrupado por `CAMIS` para que un mismo restaurante no esté a la vez en train y test) |
| **8. Feature importance** | Importancia por ganancia (`gain`) de cada variable |
| **9. Evaluación final** | Hold-out 80/20 con `GroupShuffleSplit` |

## 📊 Resultados obtenidos

**Cross-validation (5 folds, agrupado por restaurante):**

| Métrica | Media | Std |
|---|---|---|
| ROC-AUC | 0.9998 | 0.0001 |
| F1 | 0.9997 | 0.0001 |
| Precision | 0.9998 | 0.0001 |
| Recall | 0.9997 | 0.0002 |

**Hold-out set (20%):** ROC-AUC 0.9996 · F1 0.9996 · Precision 0.9999 · Recall 0.9993

**Top features (importance):** `INSPECTION TYPE_*` (varias categorías), `SCORE`, `num_violaciones`, algunos `VIOLATION CODE` puntuales (`VIOL_10B`, `VIOL_10F`).

## ⚠️ Advertencia metodológica (leer antes de usar o presentar este modelo)

Un ROC-AUC de ~0.9998 en un problema real de negocio casi siempre es señal de alarma, no de éxito.
En este caso concreto hay **fuga de información (data leakage) confirmada**:

1. **`GRADE` es una función determinista de `SCORE`**, fijada por la propia normativa del
   programa de calificación de NYC (documentado en el `.docx` oficial adjunto):
   - `SCORE < 14` → Grade **A**
   - `SCORE 14–27` → Grade **B**
   - `SCORE ≥ 28` → Grade **C**

   Como `SCORE` se incluye como feature, el modelo no está "prediciendo" nada: está
   reconstruyendo una regla aritmética que ya conocemos. La correlación `SCORE`–`target`
   (**-0.775**, la más alta de todas, muy por delante de `Latitude`/`Longitude`/mes) ya lo
   anticipaba en la Fase 4.
2. Es probable que algo similar ocurra con `INSPECTION TYPE` (el feature más importante del
   modelo): los tipos de re-inspección/reopening están mecánicamente ligados al umbral de
   `SCORE` que determina si hace falta o no una re-inspección.

**Recomendación:** si el objetivo real es útil para el negocio — por ejemplo, *anticipar* qué
restaurantes tienen más riesgo de sacar mala nota **antes** de que ocurra la inspección, para
priorizar recursos de inspección — entonces `SCORE` (y cualquier variable calculada a partir
de la misma inspección que genera el GRADE) debe **excluirse** del conjunto de features. El
modelo debería entrenarse solo con información disponible *antes* de la inspección: histórico
de violaciones previas del restaurante, tipo de cocina, ubicación, antigüedad, etc. Tal y como
está planteado ahora mismo, el pipeline resuelve un problema distinto (reconstruir la regla del
regulador) en vez del problema que interesa (anticipar el resultado).

## 🛠️ Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook index.ipynb
```

El notebook espera el CSV en `data/DOHMH_New_York_City_Restaurant_Inspection_Results_20260820.csv`;
ajusta la ruta en la primera celda de carga si lo colocas en otro sitio.

## 📁 Archivos de este módulo

```text
02_CLASIFICACION_NYC_RESTAURANTS/
├── index.ipynb                                              # Notebook con el pipeline completo
├── data/
│   └── DOHMH_New_York_City_Restaurant_Inspection_Results_*.csv
├── RestaurantInspectionDataDictionary_09242018.xlsx          # Diccionario oficial de columnas
├── About_NYC_Restaurant_Inspection_Data_on_NYC_OpenData_050222.docx
└── README.md                                                 # Este documento
```
