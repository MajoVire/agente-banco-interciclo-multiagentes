"""
Configuración global del sistema bancario
"""

# Configuración de tiempos
TIEMPO_ATENCION_MIN = 10
TIEMPO_ATENCION_MAX = 15
TIEMPO_DESCANSO = 3
TIEMPO_ENTRE_CLIENTES_MIN = 2000  # ms
TIEMPO_ENTRE_CLIENTES_MAX = 5000  # ms

# Configuración de la interfaz
TAMANO_VENTANILLAS = 3
MAX_CLIENTES_FILA = 25
UMBRAL_LIMPIEZA_FILA = 30

# Colores de la interfaz
COLORES = {
    'primary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'dark': '#2c3e50',
    'darker': '#34495e',
    'light': '#ecf0f1'
}