# TPO de Ajedrez — Ingeniería de Software

Implementación de ajedrez desarrollada para el trabajo práctico de Ingeniería de Software. El código separa las reglas del juego de la consola, utiliza una configuración clásica de 8×8, valida turnos y movimientos, registra capturas y detecta jaque. También implementa jaque mate como funcionalidad adicional.

## Ejecutar

Requiere Python 3.10 o posterior. Usa únicamente la biblioteca estándar de Python.

    python jugar.py
    python -m unittest -v

La suite contiene 37 pruebas sobre movimientos, caminos bloqueados, turnos, capturas, jaque, jaque mate, consola, dimensiones configurables y registro de piezas nuevas.

## Estructura

- ajedrez/nucleo/: tablero, piezas, movimientos y estado de la partida.
- ajedrez/adaptadores/consola.py: entrada y salida por terminal.
- tests/: pruebas que se ejecutan sin interfaz ni servicios externos.
- docs/diagrama_clases.svg: vista UML generada desde el modelo actual.
- docs/decisiones-de-diseno.docx: justificación de decisiones.
- docs/alineacion-con-la-cursada.md: contraste con la consigna y el material de clase.
- docs/presentacion-tpo.pptx: presentación del proyecto.

## Alcance

La consigna exige tablero de 8×8, seis tipos de piezas, turnos alternados, capturas, rechazo de jugadas inválidas y detección de jaque. Esta implementación también detecta jaque mate. Enroque, captura al paso, promoción, tablas, IA, deshacer/rehacer e interfaz gráfica son ampliaciones opcionales y no se presentan como funciones implementadas.

El rey no se captura: el final se determina mediante jaque mate. Una prueba de regresión cubre esta regla.

## Relación con la cursada

El diseño aplica separación entre núcleo y adaptadores, dirección de dependencias hacia el dominio, composición de reglas de movimiento, inyección de dependencias y pruebas del núcleo sin infraestructura. La consigna no exige patrones específicos; las decisiones se justifican según el problema que resuelven. El documento de alineación detalla las fuentes y los límites de la revisión.

## Copia pública

Esta copia no incluye nombres personales, número de grupo, grabaciones privadas, transcripciones ni archivos de diapositivas de la cátedra. Si se usa para entregar, el grupo puede incorporar sus datos reales en una copia privada, de acuerdo con el requisito de 3 a 5 integrantes.
