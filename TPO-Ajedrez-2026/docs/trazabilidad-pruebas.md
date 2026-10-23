# Requisitos obligatorios y pruebas representativas

Esta relación sirve como dato para el KPI de cobertura propuesto en la presentación. No mide cobertura de líneas ni reemplaza la revisión de cada prueba. Antes de entregar, el grupo debe volver a ejecutar la suite y confirmar la relación si cambió el código.

- **Tablero de 8×8:** `TestTableroInicial.test_tablero_8x8_con_32_piezas`.
- **Seis tipos de piezas y sus movimientos:** `TestMovimientoDeCadaPieza.test_peon_avanza_uno_o_dos_desde_su_fila`, `test_torre_se_frena_con_piezas`, `test_caballo_salta`, `test_alfil_en_diagonal`, `test_reina_combina_torre_y_alfil` y `test_rey_una_casilla`.
- **Turnos alternados y capturas:** `TestTurnosCapturaYValidacion.test_los_turnos_se_alternan` y `test_captura`.
- **Rechazo de movimientos inválidos:** `test_no_se_puede_mover_una_pieza_ajena`, `test_movimiento_prohibido_por_la_pieza`, `test_movimiento_invalido_no_cambia_nada` y `test_no_se_puede_capturar_al_rey_rival`.
- **Detección y protección frente al jaque:** `TestJaque.test_detecta_jaque_de_torre`, `test_detecta_jaque_de_caballo`, `test_el_peon_da_jaque_en_diagonal_y_no_de_frente` y `test_no_se_puede_dejar_al_propio_rey_en_jaque`.

Los métodos se encuentran en `tests/test_nucleo.py`. Son ejemplos representativos por requisito, no un inventario de cada caso límite. Una prueba cuenta como significativa si una aserción verifica el comportamiento esperado y falla ante una regresión relevante.
