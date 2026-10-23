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
- **10 de septiembre — Unidad 1, “Testing, TDD y TPO”, diapositivas 5–9 y 15–20.** El material respalda probar el núcleo sin infraestructura, el ciclo AAA/TDD y las pruebas de reglas de ajedrez, como el movimiento de la torre. La prueba actual de captura del rey verifica que esa jugada no se ofrezca ni se ejecute.
- **17 de septiembre — Unidad 0.1, “Tipos de Arquitectura…”, diapositivas 3 y 5–10; nota “Clase 6 17-09-2026”.** La nota disponible registra que el profesor comparó UML y código y pidió probar por módulo. El SVG se genera desde una definición manual de clases y relaciones en `docs/generar_uml.py`; esa definición y el diagrama se revisaron contra el código actual, pero no se extraen automáticamente de Python. La suite se organiza por comportamiento. La cobertura de grabación/transcripción de esa fecha es incompleta; esta afirmación se limita a la nota y a la presentación.
- **15 de octubre — Unidad 5, material bonus de IA.** El código disponible está presentado como material complementario. La IA no es una función obligatoria del núcleo y no se incluye en este repositorio. Que la consigna mencione IA como opción no convierte el bonus en requisito.

El material de la cursada también explica simular una jugada para verificar si deja al rey en jaque. Partida._deja_en_jaque copia el tablero, aplica allí el movimiento tentativo y comprueba la seguridad del rey. La clase respalda el enfoque general; no se afirma que obligue a usar exactamente esta implementación.

## Unidades 5 y 6: riesgos, métricas e integridad

Las presentaciones de Gobernanza de IT (Unidad 5, diapositivas 19 y 21–22) y Auditoría, métricas, KPIs, ética e integridad (Unidad 6, diapositivas 13 y 24–25) proponen ejercicios aplicados al TPO. El alcance de esta sección es responderlos para la defensa; no agrega requisitos funcionales al juego.

### Registro inicial de riesgos

Las probabilidades e impactos son estimaciones cualitativas para priorizar el trabajo del grupo, no resultados de una auditoría formal. En la lista, P significa probabilidad e I, impacto. Los responsables se expresan por rol para que el grupo los asigne.

- **Reglas de ajedrez mal implementadas.** Probabilidad media, impacto alto. Mitigar con pruebas vinculadas a cada requisito obligatorio y revisión de los casos límite. Responsable propuesto: quien mantiene las pruebas del núcleo.
- **Pruebas débiles o modificadas para ocultar fallas.** Probabilidad media, impacto alto. Mitigar con revisión por otro integrante y conservando aserciones que comprueben el resultado, no solo que el código se ejecute. Responsable: quien revisa cada cambio.
- **Pérdida del código o integración tardía.** Probabilidad baja, impacto alto. Mitigar con el repositorio remoto y una ejecución de la suite antes de entregar. Responsable: quien integra el trabajo.
- **Conocimiento concentrado en un integrante.** Probabilidad media, impacto medio. Mitigar con revisión compartida y una explicación del núcleo que pueda dar más de un integrante. Responsable: el grupo.
- **Exposición de una clave si se incorpora la IA opcional.** En la versión actual no hay integración de IA ni clave de API; por eso la probabilidad actual es baja y el impacto potencial sería alto. Tratamiento: evitar ese riesgo manteniendo fuera la integración opcional. Si el alcance cambiara, la clave iría fuera del repositorio y cada salida se validaría como entrada no confiable. Responsable: quien proponga la integración.

### Política breve de uso de IA

La versión actual no incorpora IA como función del juego. Si el grupo usa IA como apoyo para estudiar o escribir código, no comparte claves, credenciales ni datos personales; cada integrante revisa y entiende el código que entrega; los cambios se prueban y reciben revisión de otro integrante; y se declara el uso cuando lo pidan la consigna o las reglas de la materia. La responsabilidad por el código entregado sigue siendo del grupo.

### Meta, KPIs y KRI

**Meta:** entregar un juego que cumpla los requisitos obligatorios y cuya corrección pueda verificarse.

- **Cobertura de requisitos con pruebas:** requisitos obligatorios con al menos una prueba significativa aprobada / total de requisitos obligatorios × 100. Fuente: relación entre la consigna y `tests/test_nucleo.py`. Responsable propuesto: quien mantiene las pruebas. La prueba debe comprobar el comportamiento esperado y poder detectar una falla relevante.
- **Éxito de la suite:** pruebas aprobadas / pruebas ejecutadas × 100. Fuente: salida de `python -m unittest -v`. En la verificación de esta revisión, el resultado fue 37/37. Responsable: quien integra la versión final.
- **Revisión de cambios del núcleo:** cambios en reglas revisados por otro integrante y con la suite ejecutada / total de cambios en reglas × 100. Fuente: revisiones del repositorio y salida de tests. Responsable: quien integra; la revisión no se cuenta como válida si solo aprueba sin examinar la lógica.

**KRI:** cantidad de requisitos obligatorios que fallan o no tienen una prueba significativa. La alerta es cualquier valor mayor que cero en la verificación final; ante esa señal se dejan las ampliaciones opcionales para después y se corrige el núcleo.

Para evitar la ley de Goodhart, no se fija una meta de cantidad de tests. Se revisa que cada test corresponda a un requisito y verifique un resultado observable. Tampoco se toma la aprobación de una revisión como evidencia suficiente si no hubo lectura del cambio.

### Controles que no se agregan al producto

El ejemplo de IA de la Unidad 5 muestra un adaptador que propone una jugada y deja la validación al núcleo. Ese principio coincide con la arquitectura del proyecto, pero el ejemplo está en C# y usa una API externa; no se incorpora a esta implementación Python porque la IA es opcional y no mejora el cumplimiento del alcance obligatorio. El ejemplo de integridad en Java ilustra hashes y registros HMAC encadenados; el juego no necesita persistencia de auditoría ni protección criptográfica. Se aplican sus prácticas proporcionales —historial de cambios, revisión, tests y no ocultar defectos— sin sumar infraestructura de producción.

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
