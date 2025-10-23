    # Proyecto de Análisis Electoral con AWS Athena

Este documento resume el proceso seguido para habilitar consultas sobre resultados electorales almacenados en Amazon S3, usando **Athena** y formatos optimizados.

---

## 1. Preparación del entorno

- **Buckets de origen (raw data)**  
  - `elecciones-s3.xXXx`  
  - Contiene los JSON originales generados por Indra, con estructuras como:
    ```
    2025/pba_legislativas/backup_indra_escuelas/20250908_145358/resultados/escuelas/
    ```
  - Dentro hay ~6.800 archivos JSON por escuela, cada uno con datos de mesas esperadas, votantes, participación, y votos por agrupación.

- **Bucket de destino (para analytics)**  
  - `analytics-elecciones-s3.xXXx`  
  - Creado para almacenar los datos **normalizados** y listos para consulta con Athena.
  - Subcarpeta definida:
    ```
    athena/escuelas/
    ```

---

## 2. Creación y configuración de Athena

1. **Workgroup**  
   - Se creó un **Workgroup dedicado** llamado (ejemplo):  
     ```
     elecciones-analytics
     ```
   - Configuración:
     - **Bucket de resultados de Athena**:  
       `s3://analytics-elecciones-s3.xXXx/athena/results/`
     - **Control de costos**: límite de **500 MB por consulta** (para evitar sorpresas).
     - **Etiquetas de control**: se recomendaron tags básicos como:
       - `project = elecciones-2025`
       - `owner = tgonzalez`
       - `env = analytics`

2. **Base de datos**  
   - Creación en Athena:
     ```sql
     CREATE DATABASE elecciones;
     ```

3. **Tabla raw (escuelas_json_raw)**  
   - Primera versión para pruebas, directamente sobre los JSON en S3.  
   - Se definió con `org.openx.data.jsonserde.JsonSerDe` para poder mapear estructuras anidadas.  
   - Problema encontrado: algunos archivos estaban en formato **JSON multiline** (125 líneas), lo que generaba errores en Athena.

4. **Tabla staging/minificada (escuelas_json_min)**  
   - Para resolverlo, se creó un proceso con `jq -c` para convertir cada JSON a una **línea compacta**.  
   - Los archivos corregidos se copiaron a:
     ```
     s3://analytics-elecciones-s3.xXXx/athena/escuelas/
     ```
   - Esto permitió consultas sin errores de parseo.

---

## 3. Consideraciones de costos

- **Athena cobra por MB escaneado**, no por el número de queries.  
  - Se recomendó convertir JSON → **Parquet/ORC** con **CTAS** para optimizar y reducir costos.  
  - Se fijó un límite de 500 MB por consulta en el Workgroup.

- **S3 DataTransfer-Out (SAE1-DataTransfer-Out-Bytes)**  
  - Se detectaron cargos altos (~300 USD) que **no provinieron de los 6.800 JSON (~20 MB en total)**.  
  - La causa probable:
    - Descargas de resultados de Athena en CSV/JSON desde la consola web.
    - Descargas manuales de objetos desde S3 hacia la PC local.
  - Recomendación: mantener el análisis **dentro de AWS** y solo exportar resúmenes.

---

## 4. Buenas prácticas definidas

- **Guardar los originales** sin tocarlos (`elecciones-s3`).
- **Procesar y normalizar** los JSON con `jq -c` a un bucket separado (`analytics-elecciones-s3`).
- **Crear tablas externas en Athena** siempre apuntando a carpetas (no archivos individuales).
- **Probar con pocos archivos primero** (ejemplo `escuela_test/`) antes de cargar los 6.800.
- **Monitorear costos**:
  - Configurar Budgets en AWS con alertas de correo.
  - Usar `Cost Explorer` para revisar si los egresos vienen de S3 o Athena.

---

## 5. Estado actual

- Bucket de analytics listo:  
s3://analytics-elecciones-s3.xXXx/athena/escuelas/

markdown
Copiar código
- Workgroup configurado con límite de 500 MB.  
- Tablas creadas:
- `elecciones.escuelas_json_raw` (pruebas, con errores por formato).
- `elecciones.escuelas_json_min` (funcional, con JSON minificado).  
- Consultas básicas ejecutadas con éxito:
- Fechas de totalización.
- Cantidad de votantes.
- Participación porcentual.
- Comparaciones entre agrupaciones por escuela.

---

## 6. Próximos pasos recomendados

1. Crear una tabla optimizada con **CTAS a Parquet** para reducir costos.  
 ```sql
 CREATE TABLE elecciones.escuelas_parquet
 WITH (
   format = 'PARQUET',
   external_location = 's3://analytics-elecciones-s3.xXXx/athena/escuelas_parquet/'
 ) AS
 SELECT * FROM elecciones.escuelas_json_min;
```
Construir queries de análisis:

Ranking de participación por escuela.

Agrupación de votos por partido a nivel distrito/provincia.

Detectar escuelas con mesas faltantes.

Definir políticas de acceso (IAM) para que otros equipos puedan consultar sin riesgo de modificar datos.

7. Lecciones aprendidas
Athena requiere JSON en línea única o formato optimizado → caso de error con archivos multiline.

S3/Athena no deben usarse como almacenamiento de descargas masivas a PC local → eso genera costos altos.

Separar raw y analytics es clave para orden y performance.


Siempre configurar Budgets de costos antes de experimentar.

---
#6 Como guardar los archivos
elecciones-s3.XXXX.com.ar/2025/pba_legislativas/backup_indra_escuelas/XXXX_XXXxxxx/resultados/distrito_02_categoria_5_seccion_provincial_1_seccion_016.json

Esta es una manera de guardar los archivos lo cual no es lo mas practico para ATHENA.

Se recomienda organizar los datos en S3 utilizando prefijos con claves particionadas, de la siguiente forma:
s3://aws-elecciones/backupindra/{timestamp}/distrito_id={id}/categoria_id={id}/seccion_id={id}/escuela_id={id}/mesa_id={id}/data.json

Cada carpeta debe contener un único archivo data.json con la información correspondiente a ese nivel (mesa, escuela, sección, etc.).

```sql
s3://aws-elecciones/backupindra/2025-10-22T23:00Z/distrito_id=101/categoria_id=1/seccion_id=1/escuela_id=1/mesa_id=2300/data.json
s3://aws-elecciones/backupindra/2025-10-22T23:00Z/distrito_id=101/categoria_id=1/seccion_id=1/escuela_id=1/data.json
s3://aws-elecciones/backupindra/2025-10-22T23:00Z/distrito_id=101/categoria_id=1/data.json
```
Crear carpetas (prefijos) en Amazon S3 no tiene costo, por lo tanto esta estructura es la más eficiente y escalable para luego consultar con Athena, Glue o Redshift Spectrum.
