# HANDOFF — Sesión de 2025-09-07
# Clasificación de GRADE en inspecciones de restaurantes NYC

Copia este bloque y pégalo al inicio de una sesión nueva para que tanto Claude como tú
sepáis exactamente dónde está el proyecto, qué se hizo y qué queda pendiente.

---

```text
PROYECTO: Clasificación binaria GRADE (A vs B/C) — Restaurantes NYC DOHMH
RUTA:     pythonMaster/data_analyst/02_CLASIFICACION_NYC_RESTAURANTS/
ARCHIVOS:
  index.ipynb              ← Notebook principal (35 celdas, checklist abajo)
  README.md                ← Documentación del proyecto (⚠️ aún muestra métricas 0.999 antiguas — ver nota abajo)
  requirements.txt         ← pandas, numpy, matplotlib, seaborn, scikit-learn, xgboost, openpyxl, jupyter
  data/DOHMH_...20260820.csv  ← Dataset principal (295.473 filas × 27 col, ~152 MB)

ENTORNO: conda adk_python (Python 3.9) — con xgboost 2.1.4, sklearn 1.6.1, pandas 2.3.3
         IMPORTANTE: en el notebook NO debe aparecer `use_label_encoder=False` (eliminado — incompatible con xgboost >=2.0)

ESTADO ACTUAL DEL NOTEBOOK (35 celdas, Executes clean):
──────────────────────────────────────────────────────────
FASE 1 — Exploración:      cols, shape (295k×27), dtypes
FASE 2 — Limpieza:
  • GRADE nulos → 'unclassified'
  • Identificadores geográficos (ZIPCODE, BIN, BBL, Community Board, Council District) → object
  • Fechas parseadas (INSPECTION DATE, GRADE DATE, RECORD DATE) → año/mes, luego dropeadas
  • Investigación SCORE nulo vs GRADE unclassified (hallazgo: no es falta de evaluación)
FASE 3 — Feature Engineering:
  • clean_geo arreglado (bug original: astype(float, errors='coerce') → .pipe(pd.to_numeric, errors='coerce'))
  • Top 10 VIOLATION CODE → columnas binarias VIOL_*
  • num_violaciones por CAMIS
  • One-Hot: BORO, CRITICAL FLAG, CUISINE DESCRIPTION (top 15 + OTHER)
FASE 4 — Selección de features:
  • SCORE e INSPECTION TYPE EXCLUIDOS (data leakage — ver abajo)
  • Features finales: 36
FASE 5 — Modelado:
  • XGBClassifier (n_estimators=300, max_depth=6, lr=0.1, subsample=0.8, colsample=0.8, scale_pos_weight=balanced)
  • GroupKFold (5 folds, agrupado por CAMIS — sin restaurantes repetidos train/test)
FASE 6 — Feature Importance (gain)
FASE 7 — Hold-out 80/20 (GroupShuffleSplit) + ROC-AUC, F1, Confusion Matrix

MÉTRICAS ACTUALES (sin leakage):
  • CV 5-fold:    ROC-AUC 0.829 ± 0.005 | F1 0.842
  • Hold-out:     ROC-AUC 0.831           | F1 0.847
  (Objetivo original: ROC-AUC 0.82–0.86 — CUMPLIDO ✅)

DATA LEAKAGE — DIAGNÓSTICO Y FIX APLICADO:
──────────────────────────────────────────
Se detectó que el notebook original daba ROC-AUC 0.9998 (falso). La causa:
  1. SCORE determina GRADE directamente (regla NYC: A≤13, B=14-27, C≥28).
     Incluir SCORE como feature es una tautología → ROC-AUC 0.999.
  2. INSPECTION TYPE "Cycle Inspection/Initial" identifica la inspección que genera la nota.
     Proxy directo del resultado.
  3. Ambos han sido EXCLUIDOS del notebook actual. La celda 26 los filtra explícitamente.
  4. Verificado con experimento controlado: CON SCORE=0.9997, SIN SCORE=0.9417, SIN AMBOS=0.8280.

PROBLEMAS VISTOS Y RESUELTOS EN ESTA SESIÓN:
────────────────────────────────────────────
✅ clean_geo bug: astype(float, errors='coerce') no existe → pipe(pd.to_numeric, errors='coerce')
✅ f-string sin placeholders (lint warning F541): print(f"\nColumnas nuevas") → print("\n...")
✅ use_label_encoder=False incompatible con xgboost ≥2.0 → eliminado
✅ Corrupción texto '保持' en comentario → eliminada
✅ Data leakage de SCORE + INSPECTION TYPE → excluidos del modelo

PROBLEMAS PENDIENTES (no resueltos):
──────────────────────────────────
1. ⚠️  README.md del proyecto INCONSISTENTE: todavía muestra métricas 0.9998 (con leakage).
    Debe actualizarse para reflejar: ROC-AUC 0.83 / F1 0.85 + la nota de leakage.
2. ⚠️  Fechas 1900: INSPECTION DATE tiene filas con "01/01/1900" (placeholder).
    Inspection_year = 1900.0 para muchas filas. No están filtradas ni señaladas.
    → Opción: filtrar filas con Inspection_year < 2000, o marcarlas con flag booleano.
3. ⚠️  Grade_year / Grade_month / Record_year / Record_month: columnas con ~160k nulos (~54%).
    Comentadas en la sección de features pero nunca se eliminan formalmente de df_encoded.
    → Opción: dropearlas explícitamente tras el encoding para limpieza.
4. 💡  Modelos alternativos: RandomForest, GradientBoosting, LogisticRegression como baseline.
    Comparar con XGBoost actual.
5. 💡  Hyperparameter tuning: GridSearch/RandomizedSearch sobre max_depth, n_estimators, lr.
6. 💡  Clases desbalanceadas: clase A (76%) vs B/C (24%). scale_pos_weight ayuda, pero podría
    probarse SMOTE o class_weight más agresivo.
7. 💡  Más features temporales: extraer día de semana, si es fin de semana, estación del año
    (si la fecha 1900 se limpia primero).
8. 💡  Evaluación multiclase: A vs B vs C en vez de binario — podría ser más informativo
    para el negocio (distinguir B de C tiene valor operativo).

NOTAS PARA CLAUDE EN LA PRÓXIMA SESIÓN:
────────────────────────────────────────
• El notebook DEBE ejecutarse con el kernel de adk_python (conda), no con el Python del sistema.
• Al ejecutar, aparecen warnings de matplotlib "FigureCanvasAgg is non-interactive" — son normales en exec.
• DataFrame df_encoded se genera en celda 24 con shape (129.339, 72) tras encoding.
• features_cols se genera en celda 26 (excluyendo SCORE + INSPECTION TYPE) → 36 features.
• Para re-ejecutar: Kernel → Restart & Run All, o python -c con matplotlib.use('Agg').
• NO añadir `use_label_encoder=False` al XGBClassifier (crash con xgboost ≥2.0).
• La columna CUISINE DESCRIPTION aparece en las features tras get_dummies como CUISINE_GROUP_*,
  pero la original CUISINE DESCRIPTION no debería estar como feature (es object, no numérica).
```
