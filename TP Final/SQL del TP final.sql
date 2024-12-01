DROP TABLE IF EXISTS Orden_Producto;
DROP TABLE IF EXISTS Productos;
DROP TABLE IF EXISTS Ordenes;
DROP TABLE IF EXISTS Clientes;

CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    unidades_stock INT NOT NULL
);

CREATE TABLE Clientes (
    dni INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    domicilio VARCHAR(200) NOT NULL
);

CREATE TABLE Ordenes (
    id_orden INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    dni INT NOT NULL,
    FOREIGN KEY (dni) REFERENCES Clientes(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE Orden_Producto (
    id_orden INT auto_increment,
    id_producto INT,
    cantidad INT NOT NULL,
    PRIMARY KEY (id_orden, id_producto),
    FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE index idx_id_producto
ON Productos(id_producto);

CREATE index idx_id_orden
ON Ordenes(id_orden);

CREATE index idx_dni
ON Clientes(dni);

DROP PROCEDURE IF EXISTS ClientesQueMasGastaron;	
   
DELIMITER $$

CREATE PROCEDURE ClientesQueMasGastaron()
BEGIN 
	SELECT  c.nombre AS nombre_cliente, SUM(op.cantidad * p.precio) AS total_gastado
	FROM Clientes c
	JOIN Ordenes o ON c.dni = o.dni
	JOIN Orden_Producto op ON o.id_orden = op.id_orden
	JOIN Productos p ON op.id_producto = p.id_producto
	GROUP BY c.dni, c.nombre
	ORDER BY total_gastado DESC
	LIMIT 5;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS BuscarProductosMasVendidos()

DELIMITER $$

CREATE PROCEDURE BuscarProductosMasVendidos()
BEGIN
    SELECT p.id_producto, p.nombre, SUM(op.cantidad) AS total_vendido
    FROM Productos p
    JOIN Orden_Producto op ON p.id_producto = op.id_producto
    GROUP BY p.id_producto, p.nombre
    ORDER BY total_vendido DESC
    LIMIT 5;
END$$

DELIMITER ;


INSERT INTO Productos (nombre, precio, unidades_stock) VALUES
    ('Laptop HP', 1299.99, 100),
    ('Monitor Dell 24"', 299.99, 150),
    ('Teclado Mecánico', 89.99, 200),
    ('Mouse Gaming', 45.99, 200),
    ('Auriculares Bluetooth', 79.99, 150),
    ('Disco SSD 500GB', 129.99, 100),
    ('Memoria RAM 16GB', 89.99, 150),
    ('Webcam HD', 59.99, 100),
    ('Impresora Láser', 399.99, 50),
    ('Router WiFi', 149.99, 100);

-- Insertar Clientes
INSERT INTO Clientes (dni, nombre, domicilio) VALUES
    (11111111, 'Juan Pérez', 'Av. Principal 123'),
    (22222222, 'María García', 'Calle 45 #678'),
    (33333333, 'Carlos López', 'Plaza Central 90'),
    (44444444, 'Ana Martínez', 'Av. Libertad 234'),
    (55555555, 'Luis Rodriguez', 'Calle Norte 567'),
    (66666666, 'Laura Torres', 'Av. Sur 890'),
    (77777777, 'Pedro Sánchez', 'Calle Este 123'),
    (88888888, 'Sofia Ruiz', 'Av. Oeste 456'),
    (99999999, 'Diego Morales', 'Plaza Mayor 789'),
    (10101010, 'Carmen Díaz', 'Calle Central 012');

-- Cliente 1 (11 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
    ('2023-01-15', 1499.98, 11111111),
    ('2023-02-20', 299.99, 11111111),
    ('2023-03-15', 169.98, 11111111),
    ('2023-04-10', 479.98, 11111111),
    ('2023-05-05', 899.97, 11111111),
    ('2023-06-15', 259.98, 11111111),
    ('2023-07-20', 1399.99, 11111111),
    ('2023-08-25', 449.98, 11111111),
    ('2023-09-30', 179.98, 11111111),
    ('2023-10-15', 599.98, 11111111),
    ('2023-11-20', 289.99, 11111111);

INSERT INTO Orden_Producto VALUES
    (1, 1, 1), (1, 3, 1),     -- Laptop + Teclado
    (2, 2, 1),                -- Monitor
    (3, 3, 1), (3, 4, 1),     -- Teclado + Mouse
    (4, 2, 1), (4, 5, 1),     -- Monitor + Auriculares
    (5, 6, 2), (5, 7, 3),     -- 2 SSD + 3 RAM
    (6, 8, 2), (6, 4, 3),     -- 2 Webcam + 3 Mouse
    (7, 1, 1), (7, 5, 1),     -- Laptop + Auriculares
    (8, 9, 1), (8, 3, 1),     -- Impresora + Teclado
    (9, 4, 2), (9, 7, 1),     -- 2 Mouse + RAM
    (10, 2, 2),               -- 2 Monitores
    (11, 5, 2), (11, 8, 2);   -- 2 Auriculares + 2 Webcam

-- Cliente 2 (10 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
    ('2023-01-10', 1799.97, 22222222),
    ('2023-02-15', 449.98, 22222222),
    ('2023-03-20', 239.98, 22222222),
    ('2023-04-25', 699.97, 22222222),
    ('2023-05-30', 329.98, 22222222),
    ('2023-06-05', 1499.98, 22222222),
    ('2023-07-10', 279.98, 22222222),
    ('2023-08-15', 599.98, 22222222),
    ('2023-09-20', 189.98, 22222222),
    ('2023-10-25', 459.98, 22222222);

INSERT INTO Orden_Producto VALUES
    (12, 1, 1), (12, 2, 1), (12, 3, 1),  -- Laptop + Monitor + Teclado
    (13, 9, 1), (13, 8, 1),              -- Impresora + Webcam
    (14, 6, 1), (14, 7, 1),              -- SSD + RAM
    (15, 2, 2), (15, 5, 1),              -- 2 Monitores + Auriculares
    (16, 3, 2), (16, 4, 3),              -- 2 Teclados + 3 Mouse
    (17, 1, 1), (17, 10, 1),             -- Laptop + Router
    (18, 5, 2), (18, 8, 2),              -- 2 Auriculares + 2 Webcam
    (19, 2, 2),                          -- 2 Monitores
    (20, 4, 2), (20, 7, 1),              -- 2 Mouse + RAM
    (21, 6, 2), (21, 3, 2);              -- 2 SSD + 2 Teclados

-- Continuamos con los clientes restantes...

-- Cliente 3 (9 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-02-05', 1599.98, 33333333),
   ('2023-03-10', 399.98, 33333333),
   ('2023-04-15', 289.98, 33333333),
   ('2023-05-20', 799.97, 33333333),
   ('2023-06-25', 499.98, 33333333),
   ('2023-07-30', 1299.99, 33333333),
   ('2023-09-05', 359.98, 33333333),
   ('2023-10-10', 649.98, 33333333),
   ('2023-11-15', 429.98, 33333333);

INSERT INTO Orden_Producto VALUES
   (22, 1, 1), (22, 4, 2),              -- Laptop + 2 Mouse
   (23, 2, 1), (23, 3, 1),              -- Monitor + Teclado
   (24, 5, 2), (24, 8, 2),              -- 2 Auriculares + 2 Webcam
   (25, 9, 2),                          -- 2 Impresoras
   (26, 6, 2), (26, 7, 2),              -- 2 SSD + 2 RAM
   (27, 1, 1),                          -- Laptop
   (28, 3, 2), (28, 4, 3),              -- 2 Teclados + 3 Mouse
   (29, 2, 2), (29, 5, 1),              -- 2 Monitores + Auriculares
   (30, 9, 1), (30, 10, 1);             -- Impresora + Router

-- Cliente 4 (12 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-01-20', 1899.98, 44444444),
   ('2023-02-25', 549.98, 44444444),
   ('2023-03-30', 339.98, 44444444),
   ('2023-04-05', 899.97, 44444444),
   ('2023-05-10', 459.98, 44444444),
   ('2023-06-15', 1699.98, 44444444),
   ('2023-07-20', 299.98, 44444444),
   ('2023-08-25', 749.98, 44444444),
   ('2023-09-30', 259.98, 44444444),
   ('2023-10-05', 599.98, 44444444),
   ('2023-11-10', 399.98, 44444444),
   ('2023-12-15', 849.98, 44444444);

INSERT INTO Orden_Producto VALUES
   (31, 1, 1), (31, 2, 1), (31, 3, 1),  -- Laptop + Monitor + Teclado
   (32, 9, 1), (32, 8, 2),              -- Impresora + 2 Webcam
   (33, 6, 2), (33, 7, 1),              -- 2 SSD + RAM
   (34, 2, 3),                          -- 3 Monitores
   (35, 3, 3), (35, 4, 2),              -- 3 Teclados + 2 Mouse
   (36, 1, 1), (36, 5, 2),              -- Laptop + 2 Auriculares
   (37, 4, 3), (37, 8, 2),              -- 3 Mouse + 2 Webcam
   (38, 2, 2), (38, 10, 1),             -- 2 Monitores + Router
   (39, 5, 2), (39, 7, 1),              -- 2 Auriculares + RAM
   (40, 6, 3), (40, 3, 2),              -- 3 SSD + 2 Teclados
   (41, 9, 1),                          -- Impresora
   (42, 1, 1), (42, 4, 1);              -- Laptop + Mouse

-- Cliente 5 (10 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-01-05', 1299.99, 55555555),
   ('2023-02-10', 449.98, 55555555),
   ('2023-03-15', 269.98, 55555555),
   ('2023-04-20', 699.97, 55555555),
   ('2023-05-25', 399.98, 55555555),
   ('2023-06-30', 1499.98, 55555555),
   ('2023-08-05', 349.98, 55555555),
   ('2023-09-10', 599.98, 55555555),
   ('2023-10-15', 289.98, 55555555),
   ('2023-11-20', 799.97, 55555555);

INSERT INTO Orden_Producto VALUES
   (43, 1, 1),                          -- Laptop
   (44, 2, 1), (44, 3, 1),              -- Monitor + Teclado
   (45, 4, 3), (45, 5, 1),              -- 3 Mouse + Auriculares
   (46, 9, 1), (46, 8, 2),              -- Impresora + 2 Webcam
   (47, 6, 2), (47, 7, 1),              -- 2 SSD + RAM
   (48, 1, 1), (48, 10, 1),             -- Laptop + Router
   (49, 3, 2), (49, 4, 2),              -- 2 Teclados + 2 Mouse
   (50, 2, 2),                          -- 2 Monitores
   (51, 5, 2), (51, 8, 1),              -- 2 Auriculares + Webcam
   (52, 9, 2);                          -- 2 Impresoras

-- Cliente 6 (11 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-01-25', 1599.98, 66666666),
   ('2023-02-28', 499.98, 66666666),
   ('2023-03-25', 299.98, 66666666),
   ('2023-04-30', 899.97, 66666666),
   ('2023-05-15', 459.98, 66666666),
   ('2023-06-20', 1399.98, 66666666),
   ('2023-07-25', 259.98, 66666666),
   ('2023-08-30', 699.98, 66666666),
   ('2023-09-15', 359.98, 66666666),
   ('2023-10-20', 799.97, 66666666),
   ('2023-11-25', 399.98, 66666666);

INSERT INTO Orden_Producto VALUES
   (53, 1, 1), (53, 3, 1),              -- Laptop + Teclado
   (54, 2, 1), (54, 4, 2),              -- Monitor + 2 Mouse
   (55, 5, 2), (55, 8, 1),              -- 2 Auriculares + Webcam
   (56, 9, 2), (56, 10, 1),             -- 2 Impresoras + Router
   (57, 6, 2), (57, 7, 1),              -- 2 SSD + RAM
   (58, 1, 1), (58, 4, 1),              -- Laptop + Mouse
   (59, 3, 2),                          -- 2 Teclados
   (60, 2, 2), (60, 5, 1),              -- 2 Monitores + Auriculares
   (61, 7, 2), (61, 8, 2),              -- 2 RAM + 2 Webcam
   (62, 9, 2),                          -- 2 Impresoras
   (63, 6, 2), (63, 3, 1);              -- 2 SSD + Teclado

-- Cliente 7 (10 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-01-08', 1299.99, 77777777),
   ('2023-02-12', 399.98, 77777777),
   ('2023-03-18', 249.98, 77777777),
   ('2023-04-22', 599.97, 77777777),
   ('2023-05-28', 459.98, 77777777),
   ('2023-06-02', 1299.98, 77777777),
   ('2023-07-08', 349.98, 77777777),
   ('2023-08-12', 699.98, 77777777),
   ('2023-09-18', 289.98, 77777777),
   ('2023-10-22', 599.97, 77777777);

INSERT INTO Orden_Producto VALUES
   (64, 1, 1),                          -- Laptop
   (65, 2, 1), (65, 3, 1),              -- Monitor + Teclado
   (66, 4, 2), (66, 5, 2),              -- 2 Mouse + 2 Auriculares
   (67, 9, 1), (67, 8, 1),              -- Impresora + Webcam
   (68, 6, 2), (68, 7, 2),              -- 2 SSD + 2 RAM
   (69, 1, 1),                          -- Laptop
   (70, 3, 3), (70, 4, 1),              -- 3 Teclados + Mouse
   (71, 2, 2), (71, 10, 1),             -- 2 Monitores + Router
   (72, 5, 2), (72, 8, 1),              -- 2 Auriculares + Webcam
   (73, 9, 1), (73, 6, 1);              -- Impresora + SSD

-- Cliente 8 (9 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-02-15', 1499.98, 88888888),
   ('2023-03-20', 399.98, 88888888),
   ('2023-04-25', 269.98, 88888888),
   ('2023-05-30', 799.97, 88888888),
   ('2023-07-05', 459.98, 88888888),
   ('2023-08-10', 1199.98, 88888888),
   ('2023-09-15', 349.98, 88888888),
   ('2023-10-20', 599.98, 88888888),
   ('2023-11-25', 429.98, 88888888);

INSERT INTO Orden_Producto VALUES
   (74, 1, 1), (74, 4, 1),              -- Laptop + Mouse
   (75, 2, 1), (75, 3, 1),              -- Monitor + Teclado
   (76, 5, 2), (76, 8, 1),              -- 2 Auriculares + Webcam
   (77, 9, 2),                          -- 2 Impresoras
   (78, 6, 2), (78, 7, 1),              -- 2 SSD + RAM
   (79, 1, 1), (79, 10, 1),             -- Laptop + Router
   (80, 3, 2), (80, 4, 2),              -- 2 Teclados + 2 Mouse
   (81, 2, 2),                          -- 2 Monitores
   (82, 5, 3), (82, 8, 1);              -- 3 Auriculares + Webcam

-- Cliente 9 (10 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-01-12', 1399.98, 99999999),
   ('2023-02-18', 499.98, 99999999),
   ('2023-03-24', 289.98, 99999999),
   ('2023-04-30', 699.97, 99999999),
   ('2023-06-05', 459.98, 99999999),
   ('2023-07-12', 1299.98, 99999999),
   ('2023-08-18', 349.98, 99999999),
   ('2023-09-24', 599.98, 99999999),
   ('2023-10-30', 289.98, 99999999),
   ('2023-12-05', 799.97, 99999999);

INSERT INTO Orden_Producto VALUES
   (83, 1, 1), (83, 3, 1),              -- Laptop + Teclado
   (84, 2, 1), (84, 4, 2),              -- Monitor + 2 Mouse
   (85, 5, 2), (85, 8, 1),              -- 2 Auriculares + Webcam
   (86, 9, 1), (86, 10, 1),             -- Impresora + Router
   (87, 6, 2), (87, 7, 1),              -- 2 SSD + RAM
   (88, 1, 1),                          -- Laptop
   (89, 3, 2), (89, 4, 1),              -- 2 Teclados + Mouse
   (90, 2, 2),                          -- 2 Monitores
   (91, 5, 2), (91, 8, 1),              -- 2 Auriculares + Webcam
   (92, 9, 2);                          -- 2 Impresoras

-- Cliente 10 (8 órdenes)
INSERT INTO Ordenes (fecha, importe, dni) VALUES
   ('2023-02-08', 1599.98, 10101010),
   ('2023-03-14', 399.98, 10101010),
   ('2023-04-20', 289.98, 10101010),
   ('2023-05-26', 699.97, 10101010),
   ('2023-07-02', 459.98, 10101010),
   ('2023-08-08', 1199.98, 10101010),
   ('2023-09-14', 349.98, 10101010),
   ('2023-10-20', 599.98, 10101010);

INSERT INTO Orden_Producto VALUES
   (93, 1, 1), (93, 4, 1),              -- Laptop + Mouse
   (94, 2, 1), (94, 3, 1),              -- Monitor + Teclado
   (95, 5, 2), (95, 8, 1),              -- 2 Auriculares + Webcam
   (96, 9, 1), (96, 10, 1),             -- Impresora + Router
   (97, 6, 2), (97, 7, 1),              -- 2 SSD + RAM
   (98, 1, 1),                          -- Laptop
   (99, 3, 2), (99, 4, 2),              -- 2 Teclados
   (100, 2, 2);                          -- 2 Monitores
