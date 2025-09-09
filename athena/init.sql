-- CREATE DATABASE IF NOT EXISTS elecciones;
-- CREATE EXTERNAL TABLE IF NOT EXISTS elecciones.escuelas_json_raw (
--   json string
-- )
-- ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' -- Esto sirve para CSV no para JSON 
-- WITH SERDEPROPERTIES ('serialization.format'='1')
-- LOCATION 's3://elecciones-s3.xXXx/2025/pba_legislativas/backup_indra_escuelas/20250908_145358/resultados/escuelas/';
-- SELECT 
--   json_extract_scalar(json, '$.fechaTotalizacion') AS fecha,
--   json_extract_scalar(json, '$.estadoRecuento.cantidadVotantes') AS votantes,
--   json_extract_scalar(json, '$.estadoRecuento.participacionPorcentaje') AS participacion
-- FROM elecciones.escuelas_json_raw
-- LIMIT 10;   

-- DROP TABLE IF EXISTS elecciones.escuelas_json_raw;

-- CREATE EXTERNAL TABLE elecciones.escuelas_json_raw (
--   fechaTotalizacion string,
--   estadoRecuento struct<
--     mesasEsperadas:int,
--     mesasTotalizadas:int,
--     mesasTotalizadasPorcentaje:int,
--     cantidadElectores:int,
--     cantidadVotantes:int,
--     participacionPorcentaje:int
--   >,
--   valoresTotalizadosPositivos array<
--     struct<
--       idAgrupacion:string,
--       idAgrupacionTelegrama:string,
--       nombreAgrupacion:string,
--       votos:int,
--       votosPorcentaje:double
--     >
--   >,
--   valoresTotalizadosOtros struct<
--     votosNulos:int,
--     votosNulosPorcentaje:double,
--     votosEnBlanco:int,
--     votosEnBlancoPorcentaje:double,
--     votosRecurridosComandoImpugnados:int,
--     votosRecurridosComandoImpugnadosPorcentaje:double
--   >
-- )
-- ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
-- LOCATION 's3://elecciones-s3.xXXx/2025/pba_legislativas/backup_indra_escuelas/20250908_145358/resultados/escuelas/';

-- SELECT 
--   fechaTotalizacion
-- FROM elecciones.escuelas_json_raw
-- LIMIT 1;

-- Chequeo porque falla:
-- CREATE EXTERNAL TABLE elecciones.escuelas_staging (
--   line string
-- )
-- LOCATION 's3://elecciones-s3.xXXx/2025/pba_legislativas/backup_indra_escuelas/20250908_145358/resultados/escuelas/'
-- TBLPROPERTIES ('has_encrypted_data'='false');
-- SELECT "$path", line
-- FROM elecciones.escuelas_staging
-- WHERE line NOT LIKE '{%'
-- LIMIT 20;

-- Creamos un archivo con un solo json para entender porque falla
-- CREATE EXTERNAL TABLE elecciones.escuela_single (
--   fechaTotalizacion string,
--   estadoRecuento struct<
--     mesasEsperadas:int,
--     mesasTotalizadas:int,
--     mesasTotalizadasPorcentaje:double,
--     cantidadElectores:int,
--     cantidadVotantes:int,
--     participacionPorcentaje:double
--   >,
--   valoresTotalizadosPositivos array<
--     struct<
--       idAgrupacion:string,
--       idAgrupacionTelegrama:string,
--       nombreAgrupacion:string,
--       votos:int,
--       votosPorcentaje:double
--     >
--   >,
--   valoresTotalizadosOtros struct<
--     votosNulos:int,
--     votosNulosPorcentaje:double,
--     votosEnBlanco:int,
--     votosEnBlancoPorcentaje:double,
--     votosRecurridosComandoImpugnados:int,
--     votosRecurridosComandoImpugnadosPorcentaje:double
--   >
-- )
-- ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
-- LOCATION 's3://analytics-elecciones-s3.xXXx/athena/escuela_test/';

-- -- Creamos la nueva tabla que analiza el bucket de s3 analytics
-- CREATE EXTERNAL TABLE elecciones.escuelas_json_min (
--   fechaTotalizacion string,
--   estadoRecuento struct<
--     mesasEsperadas:double,
--     mesasTotalizadas:double,
--     mesasTotalizadasPorcentaje:double,
--     cantidadElectores:double,
--     cantidadVotantes:double,
--     participacionPorcentaje:double
--   >,
--   valoresTotalizadosPositivos array<
--     struct<
--       idAgrupacion:string,
--       idAgrupacionTelegrama:string,
--       nombreAgrupacion:string,
--       votos:double,
--       votosPorcentaje:double
--     >
--   >,
--   valoresTotalizadosOtros struct<
--     votosNulos:double,
--     votosNulosPorcentaje:double,
--     votosEnBlanco:double,
--     votosEnBlancoPorcentaje:double,
--     votosRecurridosComandoImpugnados:double,
--     votosRecurridosComandoImpugnadosPorcentaje:double
--   >
-- )
-- ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
-- LOCATION 's3://analytics-elecciones-s3.xXXx/athena/escuelas/';

WITH votos_por_escuela AS (
  SELECT
    "$path" AS archivo,  -- nombre del archivo en S3, que identifica la escuela
    v.nombreAgrupacion,
    v.votos
  FROM elecciones.escuelas_json_min
  CROSS JOIN UNNEST(valoresTotalizadosPositivos) AS t(v)
)
SELECT 
  nombreAgrupacion,
  archivo AS escuela_json,
  votos
FROM (
  SELECT 
    nombreAgrupacion,
    archivo,
    votos,
    ROW_NUMBER() OVER (PARTITION BY nombreAgrupacion ORDER BY votos DESC) AS rn
  FROM votos_por_escuela
) t
WHERE rn = 1
ORDER BY votos DESC;


