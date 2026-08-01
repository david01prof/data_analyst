# Análisis de Ventas Retail con PySpark

## 🎯 Motivación del proyecto
Como Encargado de Turno en Taco Bell durante el último año, he gestionado
operaciones diarias de tienda: turnos de personal, rotación de stock y
rendimiento por franja horaria. Este proyecto nace de una pregunta real
que me he hecho muchas veces en el día a día: **¿qué franjas horarias y
qué productos generan más rentabilidad, y cómo se puede optimizar el
personal en consecuencia?**

## 📊 Dataset
[Nombre del dataset, fuente, número de filas/columnas, breve descripción]

## 🛠️ Stack técnico
- PySpark (procesamiento y transformación de datos a escala)
- Python (Pandas para visualización final)
- Jupyter Notebook / Databricks Community Edition

## 🔍 Preguntas de negocio que respondo
1. ¿Qué productos generan más ingresos y con qué frecuencia se compran?
2. ¿Qué franjas horarias / días de la semana tienen mayor volumen de ventas?
3. ¿Existe correlación entre el canal de venta (online/local/app) y el ticket medio?
4. [Añade 1-2 preguntas más específicas de tu narrativa como encargado]

## ⚙️ Proceso
1. **Carga e ingesta**: lectura del dataset con PySpark, inferencia de esquema
2. **Limpieza**: tratamiento de nulos, duplicados, tipos de datos incorrectos
3. **Transformación**: agregaciones por producto/hora/canal usando `groupBy`, `agg`, `window functions`
4. **Análisis**: extracción de insights y visualización de resultados

## 📈 Resultados clave
[Aquí van 2-3 gráficos con su conclusión en una frase — esto es lo que más mira un reclutador]

## 💡 Conclusiones y aplicación práctica
[Cómo estos insights se traducirían en una decisión operativa real,
conectando con tu experiencia de gestión de tienda]

## 🚀 Cómo ejecutar este proyecto
```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_exploracion.ipynb
```