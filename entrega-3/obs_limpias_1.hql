 -- Creacion de una Base de Daots con los registros limpios
CREATE DATABASE base_de_datos_observaciones;
USE base_de_datos_observaciones;

 -- Datos con su significado y tipo correspondiente
CREATE TABLE observaciones(
        tipo_de_calibracion string,
        tiempo_en_ascencion_recta time,
        tiempo_en_declinacion time,
        fecha_y_hora_de_observacion datetime,
        codigo_asignado_eso string,
        investigadores string,
        tipo_de_observador string,
        titulo_de_proyecto string,
        tipo_de_programa string,
        tipo_de_instrumento string,
        tipo_de_archivo string,
        tipo_de_calibracion string,
        modo_de_observacion string,
        nombre_unico string,
        nombre_fits string,
        fecha_de_observacion date,
        objeto_observado string,
        codigo_observatorio string,
        pipeline_de_reduccion string,
        tiempo_de_finalizacion time
        redshift float
        longitud_onda_central float,
        longitud_onda_final float,
        modo_de_adquisicion string,
        dispersor_usado string,
        configuracion_espectral string,
        geometria_de_rendija string,
        fecha_julian_date double,
        airmass float,
        seeing float,
        null_0 string,
        null_1 string,
        null_2 string
)
 -- Darles el formato de lectura separado por comas
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';
 -- Leer registros desde el archivo subido al DFS
LOAD DATA INPATH '/data/vlt_observations_000_clean.csv' INTO TABLE observaciones;