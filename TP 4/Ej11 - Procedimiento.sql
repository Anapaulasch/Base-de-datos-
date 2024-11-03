DELIMITER $$
CREATE PROCEDURE GenerarResumenDiario()
BEGIN
	
    DECLARE finCursor BOOLEAN DEFAULT FALSE;
    DECLARE linea VARCHAR(50);
    DECLARE fecha DATE;
    DECLARE total INT;
    
    DECLARE cursorResumen CURSOR FOR 
		SELECT DISTINCT LineaProduccion, FechaProduccion 
		FROM Produccion;
	
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finCursor = TRUE;
    
    TRUNCATE TABLE resumenproduccion;
    
    OPEN cursorResumen;
    FETCH cursorResumen INTO linea, fecha;
	WHILE finCursor IS FALSE DO
		 		
        SELECT sum(CantidadProducida) INTO total
        FROM produccion
        WHERE LineaProduccion = linea AND FechaProduccion = fecha;
		
        IF total IS NOT NULL THEN
			START TRANSACTION;
				INSERT INTO resumenproduccion(LineaProduccion, FechaProduccion, TotalProducido) VALUES (linea, fecha, total);
			COMMIT;
        END IF;
        FETCH cursorResumen INTO linea, fecha;
	END WHILE;
    
    CLOSE cursorResumen;

END$$
DELIMITER ;
