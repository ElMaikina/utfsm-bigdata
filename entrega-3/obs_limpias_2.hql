...

 -- Agrupar en base a los modos de observacion mas comunes
SELECT modo_de_observacion, COUNT(*) AS cantidad
FROM observaciones
GROUP BY modo_de_observacion;

 -- Tiempo promedio en declinacion por cada tipo de instrumento
SELECT tipo_de_instrumento, AVG(tiempo_en_declinacion) AS promedio_declinacion
FROM observaciones
GROUP BY tipo_de_instrumento;

 -- Seeing promedio por hora de observacion
SELECT HOUR(fecha_y_hora_de_observacion) AS hora, AVG(seeing) AS promedio_seeing
FROM observaciones
GROUP BY HOUR(fecha_y_hora_de_observacion)
ORDER BY hora;