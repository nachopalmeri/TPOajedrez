# Revisión de alineación con la cursada

## Conclusión

El proyecto cumple el alcance obligatorio del TPO y las pautas de ingeniería que aparecen en el material disponible. El defecto funcional más claro era que una torre podía capturar al rey rival. Se bloqueó esa jugada al generar movimientos legales, al ejecutar un movimiento y al buscar movimientos disponibles para detectar jaque mate. Una prueba de regresión cubre el caso. La suite tiene 37 pruebas aprobadas.

La consigna no impone patrones de diseño concretos; el material de clase también advierte que no conviene forzar patrones sin necesidad. Por eso, la revisión contrasta comportamientos y justificaciones con la cursada, sin convertir los nombres de patrones en requisitos.

## Consigna oficial

Fuente: TPO_Ingenieria de Software_Dominio Ajedrez.docx. Está en la carpeta de la materia y no se copia a este repositorio público.

La consigna pide:

- Tablero de 8×8 y los seis tipos de piezas con sus movimientos.
- Turnos alternados, capturas, rechazo de movimientos inválidos y detección de jaque.
- Núcleo independiente de frameworks e infraestructura, pruebas unitarias que puedan ejecutarse sin servicios externos y un UML coherente con la implementación.
- Una justificación breve que explique qué decisión se tomó, por qué y en qué situación podría dejar de convenir.
- Presentación grupal y defensa individual. El grupo debe tener entre 3 y 5 integrantes.

La consigna enumera como opcionales el jaque mate, el enroque, la captura al paso, la promoción, las tablas, la IA, deshacer/rehacer y una interfaz gráfica más allá de la consola mínima. El proyecto incluye jaque mate, pero no declara implementadas las demás extensiones.

## Cruce con las clases

Las fechas corresponden a las presentaciones y notas disponibles. El repositorio no redistribuye las diapositivas ni las transcripciones de la cátedra; se indican sus nombres y secciones para que puedan localizarse.

- **6 de agosto — Unidad 1, “Ingeniería y Diseño”, diapositivas 10–18.** Presenta separación entre núcleo y adaptadores, dirección de dependencias, arquitectura hexagonal y testabilidad. Las reglas están en ajedrez/nucleo/ y la interacción de terminal en ajedrez/adaptadores/consola.py.
- **13 de agosto — nota “Clase 2 13-08-26”.** Continúa el análisis de arquitectura. Partida no lee ni imprime, por lo que las pruebas pueden invocar directamente las reglas.
- **20 de agosto — Unidad 1, “SOLID, Dependency Injection y Composition”, diapositivas 2, 9–10 y 18.** Trata SOLID, inyección por constructor, composición y elección de patrones por necesidad. Partida recibe Disposicion y CatalogoDePiezas como dependencias opcionales; cada Pieza compone comportamientos de movimiento. El catálogo permite registrar una pieza nueva sin modificar las clases existentes. Son decisiones del diseño, no patrones obligatorios por la consigna.
- **27 de agosto — Unidad 1, “Patrones y Testing”, diapositivas 12 y 15–17.** Command y State aparecen como herramientas, y deshacer como extensión opcional del ajedrez. No se agregan esos patrones solamente para demostrar que se conocen.
- **10 de septiembre — Unidad 1, “Testing, TDD y TPO”, diapositivas 5–9 y 15–20.** El material respalda probar el núcleo sin infraestructura, el ciclo AAA/TDD y las pruebas de reglas de ajedrez, como el movimiento de la torre. La regresión de captura del rey se agregó primero como prueba: falló porque a8 aparecía como destino legal de la torre y pasó después de corregir la regla.
- **17 de septiembre — Unidad 0.1, “Tipos de Arquitectura…”, diapositivas 3 y 5–10; nota “Clase 6 17-09-2026”.** La nota disponible registra que el profesor comparó UML y código y pidió probar por módulo. El diagrama UML incluido se genera desde las clases del proyecto y la suite se organiza por comportamiento. La cobertura de grabación/transcripción de esa fecha es incompleta; esta afirmación se limita a la nota y a la presentación.
- **15 de octubre — Unidad 5, material bonus de IA.** El código disponible está presentado como material complementario. La IA no es una función obligatoria del núcleo y no se incluye en este repositorio. Que la consigna mencione IA como opción no convierte el bonus en requisito.

El material de la cursada también explica simular una jugada para verificar si deja al rey en jaque. Partida._deja_en_jaque copia el tablero, aplica allí el movimiento tentativo y comprueba la seguridad del rey. La clase respalda el enfoque general; no se afirma que obligue a usar exactamente esta implementación.

## Defecto corregido

Antes de la corrección, Partida.movimientos_legales podía incluir una casilla ocupada por el rey rival. Partida.mover aceptaba esa captura y quitaba al rey del tablero, lo que rompía el modelo de jaque y jaque mate.

Ahora el núcleo filtra la captura del rey de los movimientos legales, la excluye al buscar movimientos disponibles y rechaza el intento directo de ejecutarla. La prueba verifica que la jugada no se ofrece, que mover lanza MovimientoInvalido, que el rey sigue en el tablero y que ni el turno ni el historial cambian. El jaque mate se detecta mediante es_jaque_mate.

Verificación: python -m unittest -v — 37 pruebas aprobadas en la copia revisada.

## Decisiones para defender

- **Núcleo y adaptador de consola:** permite usar las reglas desde pruebas u otra interfaz. Aporta menos si el programa fuera una consola descartable sin necesidad de pruebas ni reutilización.
- **Composición de movimientos:** combina comportamientos de movimiento. Se vuelve menos clara si aparecen muchas piezas con interacciones particulares que no pueden expresarse con esas reglas.
- **Destinos y ataques:** los peones avanzan y capturan de formas distintas. Una variante con reglas de ataque más complejas podría requerir un modelo más expresivo.
- **Catálogo de piezas:** registra fábricas y permite extensiones. Es indirección innecesaria si el juego siempre tendrá el mismo conjunto de piezas y nunca se extenderá.
- **Configuración de disposición y tamaño:** facilita pruebas controladas y la defensa de extensibilidad. Agrega casos para validar si el tablero y la disposición fueran siempre fijos.
- **Copia del tablero para validar:** evita alterar la partida real al simular una jugada. Puede tener costo si el tablero o la cantidad de validaciones crecieran mucho; una alternativa incremental debería justificarse con mediciones.
- **Posiciones y piezas inmutables:** reduce cambios laterales inesperados. Puede ser incómodo si una variante necesita editar con frecuencia las propiedades internas de las piezas.

La explicación completa en formato qué, por qué y cuándo dejaría de ser adecuada está en decisiones-de-diseno.docx.

## Límites de alcance

No se afirma que estén implementados el enroque, la captura al paso, la promoción, las tablas, la IA, deshacer/rehacer o una interfaz gráfica. Su ausencia coincide con la lista de ampliaciones opcionales de la consigna. Tampoco se copia al repositorio el código bonus de IA de la materia.

## Límites de las fuentes

La revisión usó la consigna oficial, las presentaciones y notas disponibles, el código y las pruebas del proyecto. Algunas grabaciones no tenían transcripción correspondiente; además, al menos una transcripción disponible era parcial o ruidosa. Por eso no se afirma haber comprobado cada minuto de todas las grabaciones. El cruce de fechas indica únicamente lo que se pudo respaldar con las notas y presentaciones encontradas. El texto de la revisión previa que motivó esta búsqueda no apareció como archivo independiente; se localizaron el proyecto y sus fuentes por separado.

## Límites de la copia pública

El repositorio omite nombres personales, correos, número de grupo, rutas locales de Windows, archivos de la materia, grabaciones, transcripciones y código bonus provisto por la cátedra. La consigna exige identificar al grupo en el contexto de entrega; agreguen la nómina real en una copia privada después de confirmarla con todos sus integrantes. No se publican nombres en esta copia.
