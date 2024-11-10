**Esquema de BD:**

JUEGO `<año_olimpiada, pais_olimpiada, nombre_deportista, pais_deportista, nombre_disciplina, asistente>`

**Restricciones:**

a. `pais_olimpiada` es el país donde se realizó el juego olímpico del año correspondiente.

b. `pais_deportista` es el país que representa el deportista.

c. Un deportista representa en todos los juegos olímpicos 
siempre al mismo país. Por un
país, participan varios deportistas cada juego olímpico.  

d. En un año determinado se hacen los juegos olímpicos en un solo país, pero en un país
pueden haberse jugados varios juegos olímpicos en diferentes años.

e. Cada deportista puede participar en varios juegos olímpicos y en varias disciplinas en
diferentes juegos olímpicos. Pero en un juego olímpico solamente participa en una
disciplina.

f. Un deportista tiene un asistente en cada juego olímpico, pero puede variar en diferentes
juegos.

---
### Paso 1: Determinar las Dependencias Funcionales (DFs)

**`año_olimpiada` -> `pais_olimpiada`**: `pais_olimpiada` depende funcionalmente de `año_olimpiada` porque cada año que se realiza un juego olimpico se realiza en un unico pais.

**`nombre_deportista` -> `pais_deportista`**: `pais_deportista` depende funcionalmente de `nombre_deportista` porque un deportista representa siempre al mismo país en todos los juegos olímpicos 

**`año_olimpiada`, `nombre_deportista` -> `nombre_disciplina`**: un deportista puede participar en varios juegos olimpicos y en varias disciplinas pero en un juego olimpico especifico (determinado por el año y el deportista) solo puede participar en una disciplina.
Por lo tanto `nombre_disciplina` depende funcionalmente de `año_olimpiada` y `nombre_deportista` 

**`año_olimpiada`, `nombre_deportista` -> `asistente`**: Cada deportista tiene un asistente en cada juego olímpico, pero este asistente puede variar en diferentes juegos. Esto significa que el asistente de un deportista en un juego olímpico específico está determinado por el año y el nombre del deportista. Por lo tanto `asistente` depende funcionalmente de `año_olimpiada` y `nombre_deportista` 

---
### Paso 2 determinar la clave candidata

La combinacion de año_olimpiada y nombre_deportista es suficiente para identificar de forma unica cada registro en la tabla, ya que:

- `año_olimpiada` identifica el año en el que se realiza el juego olímpico.
- `nombre_deportista` identifica el deportista que compite en el juego olimpico de ese año.

Por lo que la clave candidata es: (año_olimpiada, nombre_deportista)

Esto asegura que no haya registros duplicados en la tabla.

---
### Paso 3 : Diseño en Tercera Forma Normal(3fn)

1. **Tabla `Participaciones`:**
    - `año_olimpiada` (Clave foranea que referencia a `JuegosOlimpicos`)
    - `nombre_deportista` (Clave foranea que referencia a `Deportistas`)
    - `asistente`
    - `nombre_disciplina`
    - clave primaria compuesta: (`año_olimpiada`, `nombre_deportista`)

1. **Tabla `JuegosOlimpicos`:**
    - `año_olimpiada` (Clave primaria)
    - `pais_olimpiada`

1. **Tabla `Deportistas`:**
    - `nombre_deportista` (Clave primaria)
    - `pais_deportista`





