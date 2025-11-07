#!/usr/bin/env python3
"""
Punto de entrada principal del Sistema de Gestión Bancaria
"""

import tkinter as tk
from views.interfaz_banco import InterfazBanco

def main():
    """Función principal que inicia la aplicación"""
    try:
        root = tk.Tk()
        app = InterfazBanco(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()