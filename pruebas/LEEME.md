# Pruebas de la app

Pruebas automáticas (Playwright, Python) que se pasan en móvil (390×844) y en PC antes de publicar cada cambio.

- `mockfb.js`: imitación de Firebase para probar sin tocar los datos reales.
- `tform2.py` y `tportadas.py`: base común (datos de prueba inventados y arranque de la página).
- El resto (`t*.py`): una prueba por función (copias, garantía, tickets, circuito, QR…).

Los datos que aparecen son inventados. Se ejecutan con `python3 pruebas/<archivo>.py` ajustando las rutas del principio de cada archivo.
