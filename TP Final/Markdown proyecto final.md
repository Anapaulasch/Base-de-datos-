1. **Tabla Productos:**
	- `id_producto` (Clave primaria)
	- `nombre`
	- `precio`	
	- `unidades_stock`

**`id_producto` -> `nombre`, `precio`, `unidades_stock`:** `id_producto` es único para cada producto y determina los atributos `nombre`, `precio` y `unidades_stock`.
Por lo tanto el nombre, precio y cantidad de unidades en stock del producto dependen de `id_producto`.

El uso del atributo `id_producto` es suficiente para identificar de manera unica cada registro en la tabla ya que `nombre`, `precio` y `unidades_stock` dependen de `id_producto`.

---
2. **Tabla `Clientes`:**
	- `dni` (Clave primaria)
	- `nombre`
	- `domicilio` 
	
**`dni` -> `nombre`, `domicilio`:** el dni es único para cada cliente y determina los atributos nombre y domicilio.
Por lo tanto el nombre y el domicilio del cliente dependen del dni.

El uso del atributo dni como clave primaria es suficiente para identificar de manera unica cada registro en la tabla ya que nombre y domicilio dependen de dni.

---
3. **Tabla `Ordenes`:**
	- `id_orden` (Clave primaria)
	- `fecha`
	- `importe`	
	- `dni` (Clave foranea que referencia a Clientes)

**`id_orden` -> `fecha`, `importe`, `dni`:** `id_orden` es único para cada orden y determina los atributos `fecha`, `importe` y `dni`.
Por lo tanto la fecha, el importe y el dni (que indica el cliente relacionado a la orden) de la orden dependen del `id_orden`.

El uso del atributo id_orden como clave primaria es suficiente para identificar de manera unica cada registro en la tabla ya que fecha e importe dependen del id_orden

---
4. **Tabla `Orden_producto`:**
	- `id_orden` (Clave foranea que referencia a `Ordenes`)
	- `id_producto` (Clave foranea que referencia a `Productos`)
	- `cantidad`
	- clave primaria compuesta: (`id_orden`, `id_producto`)

**`id_orden`, `id_producto` -> `cantidad`:** `cantidad` expresa la cantidad del producto que hay en la orden, por lo que depende de `id_orden` e `id_producto`.

El uso de los atributos `id_orden` e `id_producto` es requerido para identificar de manera unica cada registro en la tabla ya que cantidad depende de ambos `id_orden` e `id_producto`.
