import tkinter as tk
import random
import time
from PIL import Image, ImageTk, ImageDraw

from models.banco import Banco
from models.persona import Persona

class InterfazBanco:
    """
    Interfaz gráfica para el sistema de gestión bancaria
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica
        """
        self.root = root
        self.setup_ventana_principal()
        self.setup_estilos()
        self.setup_imagenes()
        self.setup_banco()
        self.setup_interfaz()
        
        # Control de escenario activo
        self.escenario_activo = None  # None, "con_prioridad", "sin_prioridad"
        self.simulacion_activa = False

    def setup_ventana_principal(self):
        """Configura la ventana principal"""
        self.root.title("Sistema de Gestión Bancaria - Simulación Inteligente")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
    
    def setup_estilos(self):
        """Configura los estilos visuales"""
        self.colores = {
            'primary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#2c3e50',
            'darker': '#34495e',
            'light': '#ecf0f1',
            'notification': '#9b59b6'
        }
    
    def setup_imagenes(self):
        """Carga y configura las imágenes con manejo robusto de errores"""
        # Configuración de tamaños
        self.TAMANO_CLIENTE = (30, 30)
        self.TAMANO_PRIORITARIO = (30, 30)
        self.TAMANO_VENTANILLA = (60, 60)
        self.TAMANO_CELULAR = (140, 220)
        
        # Lista de imágenes a cargar
        imagenes_info = [
            ("imagenes/cliente_normal.png", "cliente"),
            ("imagenes/cliente_prioritario.png", "prioritario"),
            ("imagenes/ventanilla.png", "ventanilla"),
            ("imagenes/celular.png", "celular")
        ]
        
        for ruta, nombre in imagenes_info:
            try:
                # Determinar tamaño según tipo de imagen
                if nombre == 'celular':
                    tamaño = self.TAMANO_CELULAR
                else:
                    tamaño = getattr(self, f'TAMANO_{nombre.upper()}')
                
                # Cargar y redimensionar imagen
                imagen = Image.open(ruta)
                imagen_redimensionada = imagen.resize(tamaño)
                imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
                setattr(self, f'img_{nombre}', imagen_tk)
                print(f"✅ Imagen {ruta} cargada correctamente")
                
            except FileNotFoundError:
                print(f"❌ No se encontró: {ruta}")
                self.crear_placeholder_imagen(nombre)
            except Exception as e:
                print(f"❌ Error cargando {ruta}: {e}")
                self.crear_placeholder_imagen(nombre)

    def crear_placeholder_imagen(self, tipo_imagen):
        """Crea placeholders con colores diferentes para cada tipo"""
        colores_placeholder = {
            'cliente': '#3498db',      # Azul
            'prioritario': '#e74c3c',  # Rojo
            'ventanilla': '#27ae60',   # Verde
            'celular': '#9b59b6'       # Púrpura
        }
        
        color = colores_placeholder.get(tipo_imagen, '#95a5a6')
        tamaño = self.TAMANO_CELULAR if tipo_imagen == 'celular' else self.TAMANO_CLIENTE
        
        # Crear imagen de color sólido
        imagen = Image.new('RGB', tamaño, color)
        
        # Agregar texto identificador
        draw = ImageDraw.Draw(imagen)
        try:
            texto = tipo_imagen.upper()[:3]
            draw.text((tamaño[0]//2, tamaño[1]//2), texto, fill='white', anchor='mm')
        except Exception:
            pass
        
        imagen_tk = ImageTk.PhotoImage(imagen)
        setattr(self, f'img_{tipo_imagen}', imagen_tk)
        print(f"🔄 Placeholder creado para {tipo_imagen}")
    
    def setup_banco(self):
        """Inicializa el sistema bancario"""
        self.banco = Banco(n_ventanillas=3, interfaz=self)
        self.personas_en_fila_gui = []
        self.ventanillas_gui = []
        self.dispositivos_moviles = []
    
    def setup_interfaz(self):
        """Configura todos los elementos de la interfaz gráfica"""
        self.setup_header()
        self.setup_paneles_principales()
        self.setup_panel1_ventanillas()
        self.setup_panel2_fila_notificaciones()
        self.setup_panel3_estadisticas_controles()
        self.setup_log_tags()
    
    def setup_header(self):
        """Configura el header de la aplicación"""
        self.header_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.header_frame, text="🏢 BANCO ESTRELLA", 
                font=("Arial", 20, "bold"), bg='#34495e', fg='white').pack(pady=10)
        tk.Label(self.header_frame, text="Sistema de Gestión de Colas Inteligente", 
                font=("Arial", 12), bg='#34495e', fg='#ecf0f1').pack(pady=(0, 10))
    
    def setup_paneles_principales(self):
        """Configura los paneles principales - DISTRIBUCIÓN OPTIMIZADA"""
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # PANEL 1: Ventanillas de atención (más compacto)
        self.panel1 = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2, width=400)  # Reducido
        self.panel1.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        self.panel1.pack_propagate(False)

        # PANEL 2: Fila de clientes + Notificaciones (tamaño equilibrado)
        self.panel2 = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        self.panel2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        # PANEL 3: Controles + Logs (más ancho para el registro)
        self.panel3 = tk.Frame(main_frame, bg='#34495e', width=500, relief='raised', bd=2)  # Aumentado
        self.panel3.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.panel3.pack_propagate(False)
    
    def setup_panel1_ventanillas(self):
        """Configura el PANEL 1: Ventanillas de atención"""
        tk.Label(self.panel1, text="VENTANILLAS DE ATENCIÓN", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=15)

        ventanillas_frame = tk.Frame(self.panel1, bg='#34495e')
        ventanillas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Crear interfaz para cada ventanilla
        for ventanilla in self.banco.ventanillas:
            self._crear_ventanilla_gui(ventanilla, ventanillas_frame)
    
    def _crear_ventanilla_gui(self, ventanilla, parent_frame):
        """Crea la interfaz gráfica para una ventanilla individual"""
        vent_frame = tk.Frame(parent_frame, bg='#2c3e50', relief='solid', bd=1)
        vent_frame.pack(fill=tk.X, padx=10, pady=10)
        
        card_frame = tk.Frame(vent_frame, bg='white', relief='raised', bd=2)
        card_frame.pack(fill=tk.X, padx=8, pady=8)
        
        # Header de la ventanilla
        header_vent = tk.Frame(card_frame, bg='#3498db', height=30)
        header_vent.pack(fill=tk.X)
        header_vent.pack_propagate(False)
        
        tk.Label(header_vent, text=f"Ventanilla {ventanilla.id}", 
                font=("Arial", 12, "bold"), bg='#3498db', fg='white').pack(expand=True)
        
        # Contenido de la ventanilla
        content_vent = tk.Frame(card_frame, bg='white', height=100)
        content_vent.pack(fill=tk.X, padx=8, pady=8)
        content_vent.pack_propagate(False)
        
        # Imagen de la ventanilla
        img_frame = tk.Frame(content_vent, bg='white', width=80)
        img_frame.pack(side=tk.LEFT, fill=tk.Y)
        img_frame.pack_propagate(False)
        
        img_label = tk.Label(img_frame, image=self.img_ventanilla, bg='white')
        img_label.pack(expand=True, padx=5)
        
        # Información de la ventanilla
        info_frame = tk.Frame(content_vent, bg='white')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        # Labels para mostrar información
        estado_label = tk.Label(info_frame, text="LIBRE", 
                              font=("Arial", 11, "bold"), bg='white', fg='#27ae60',
                              justify=tk.LEFT)
        estado_label.pack(anchor=tk.W, pady=(0, 3))
        
        cliente_label = tk.Label(info_frame, text="", 
                               font=("Arial", 10), bg='white', fg='#7f8c8d',
                               justify=tk.LEFT)
        cliente_label.pack(anchor=tk.W, pady=(0, 3))
        
        transaccion_label = tk.Label(info_frame, text="", 
                                   font=("Arial", 9), bg='white', fg='#9b59b6',
                                   justify=tk.LEFT, wraplength=250)
        transaccion_label.pack(anchor=tk.W, pady=(0, 3))
        
        tiempo_label = tk.Label(info_frame, text="", 
                              font=("Arial", 9), bg='white', fg='#e74c3c',
                              justify=tk.LEFT)
        tiempo_label.pack(anchor=tk.W)
        
        # Almacenar referencia a los elementos GUI de la ventanilla
        self.ventanillas_gui.append({
            'frame': card_frame,
            'header': header_vent,
            'estado': estado_label,
            'cliente': cliente_label,
            'transaccion': transaccion_label,
            'tiempo': tiempo_label,
            'imagen': img_label,
            'ventanilla': ventanilla
        })
    
    def setup_panel2_fila_notificaciones(self):
        """Configura el PANEL 2: Fila de clientes + Notificaciones móviles"""
        
        # Sección FILA DE CLIENTES
        fila_frame = tk.Frame(self.panel2, bg='#34495e')
        fila_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(fila_frame, text="FILA DE CLIENTES", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        # Canvas para mostrar la fila con scroll horizontal
        fila_canvas_frame = tk.Frame(fila_frame, bg='#ecf0f1', relief='sunken', bd=2)
        fila_canvas_frame.pack(fill=tk.X, pady=5)

        self.h_scrollbar = tk.Scrollbar(fila_canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas_fila = tk.Canvas(fila_canvas_frame, height=80, bg='#ecf0f1',
                                   xscrollcommand=self.h_scrollbar.set)
        self.canvas_fila.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.h_scrollbar.config(command=self.canvas_fila.xview)

        # Leyenda de colores
        self._crear_leyenda_fila(fila_frame)

        # Separador
        separator = tk.Frame(self.panel2, height=2, bg='#7f8c8d')
        separator.pack(fill=tk.X, padx=20, pady=10)

        # Sección NOTIFICACIONES MÓVILES
        self._setup_notificaciones_moviles()
    
    def _crear_leyenda_fila(self, parent_frame):
        """Crea la leyenda para los tipos de clientes en la fila"""
        legend_frame = tk.Frame(parent_frame, bg='#34495e')
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="Leyenda: ", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(side=tk.LEFT)
        tk.Label(legend_frame, text="● Normal", font=("Arial", 9), 
                bg='#34495e', fg='black').pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="● Prioritario", font=("Arial", 9), 
                bg='#34495e', fg='red').pack(side=tk.LEFT, padx=5)
    
    def _setup_notificaciones_moviles(self):
        """Configura la sección de notificaciones móviles"""
        notif_frame = tk.Frame(self.panel2, bg='#34495e')
        notif_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(notif_frame, text="📱 NOTIFICACIONES MÓVILES POR VENTANILLA", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        dispositivos_frame = tk.Frame(notif_frame, bg='#34495e')
        dispositivos_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Crear dispositivos móviles para cada ventanilla
        for i in range(3):
            self._crear_dispositivo_movil(dispositivos_frame, i + 1)
    
    def _crear_dispositivo_movil(self, parent_frame, ventanilla_id):
        """Crea un dispositivo móvil para una ventanilla específica"""
        dispositivo_frame = tk.Frame(parent_frame, bg='#34495e')
        dispositivo_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=8)
        
        # Etiqueta de la ventanilla
        tk.Label(dispositivo_frame, text=f"Ventanilla {ventanilla_id}", 
                font=("Arial", 11, "bold"), bg='#34495e', fg='white').pack(pady=(0, 8))
        
        # Simulación de dispositivo móvil
        celular_frame = tk.Frame(dispositivo_frame, bg='#1a1a1a', relief='sunken', bd=3, 
                               width=160, height=240)
        celular_frame.pack(pady=5)
        celular_frame.pack_propagate(False)

        celular_display = tk.Frame(celular_frame, bg='#2c3e50')
        celular_display.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        notif_celular_frame = tk.Frame(celular_display, bg='#ecf0f1')
        notif_celular_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Label para mostrar notificaciones
        notificacion_label = tk.Label(notif_celular_frame, 
                                    text="Esperando...",
                                    font=("Arial", 9),
                                    bg='#ecf0f1', fg='#7f8c8d',
                                    wraplength=130,
                                    justify=tk.LEFT)
        notificacion_label.pack(expand=True, padx=5, pady=5)

        # Estado del dispositivo
        estado_label = tk.Label(dispositivo_frame, text="🟢 Listo",
                              font=("Arial", 9),
                              bg='#34495e', fg='#27ae60')
        estado_label.pack(pady=5)

        # Almacenar referencia al dispositivo
        self.dispositivos_moviles.append({
            'frame': dispositivo_frame,
            'celular': celular_frame,
            'notificacion': notificacion_label,
            'estado': estado_label,
            'ventanilla_id': ventanilla_id,
            'ultima_notificacion': None
        })
    
    def setup_panel3_estadisticas_controles(self):
        """Configura el PANEL 3: Estadísticas + Controles"""
        
        # Sección ESTADÍSTICAS
        stats_frame = tk.Frame(self.panel3, bg='#2c3e50', relief='solid', bd=1)
        stats_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(stats_frame, text="ESTADÍSTICAS EN TIEMPO REAL", 
                font=("Arial", 14, "bold"), bg='#2c3e50', fg='white').pack(pady=10)

        self.stats_label = tk.Label(stats_frame, 
                text="Ventanillas libres: 3/3\nClientes en fila: 0\nClientes atendidos: 0",
                font=("Arial", 12), bg='#2c3e50', fg='#ecf0f1', justify=tk.LEFT)
        self.stats_label.pack(pady=10)

        # Separador
        separator = tk.Frame(self.panel3, height=2, bg='#7f8c8d')
        separator.pack(fill=tk.X, padx=20, pady=10)

        # Sección CONTROLES
        self._setup_controles()
    
    def _setup_controles(self):
        """Configura los botones de control - VERSIÓN COMPACTA"""
        controls_frame = tk.Frame(self.panel3, bg='#34495e')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)  # Reducir padding

        tk.Label(controls_frame, text="CONTROLES", 
                font=("Arial", 12, "bold"), bg='#34495e', fg='white').pack(pady=(0, 8))  # Fuente más pequeña

        # Estilo para botones COMPACTOS
        compact_button_style = {
            'font': ('Arial', 9),  # Fuente más pequeña
            'pady': 4,            # Menos padding vertical
            'padx': 8,            # Menos padding horizontal  
            'height': 1           # Altura fija mínima
        }

        # Botones de demostración COMPACTOS
        tk.Button(controls_frame, text="🎭 1 - Con Prioridad", 
                command=self.demo_escenario_1, bg='#9b59b6', fg='white',
                **compact_button_style).pack(fill=tk.X, pady=2)  # Menos espacio entre botones

        tk.Button(controls_frame, text="🎭 2 - Sin Prioridad", 
                command=self.demo_escenario_2, bg='#3498db', fg='white',
                **compact_button_style).pack(fill=tk.X, pady=2)

        tk.Button(controls_frame, text="👑 3 - Solo Prioritarios", 
                command=self.demo_escenario_3, bg='#e67e22', fg='white',
                **compact_button_style).pack(fill=tk.X, pady=2)

        tk.Button(controls_frame, text="🔴 4 - Ventanillas Ocupadas", 
                command=self.demo_escenario_4, bg='#e74c3c', fg='white',
                **compact_button_style).pack(fill=tk.X, pady=2)

        # Botón adicional para limpiar/reiniciar (opcional)
        tk.Button(controls_frame, text="🔄 Reiniciar Sistema", 
                command=self.reiniciar_sistema, bg='#95a5a6', fg='white',
                **compact_button_style).pack(fill=tk.X, pady=2)

        # Sección REGISTRO DE ACTIVIDAD
        self._setup_registro_actividad()

    def limpiar_log(self):
        """Limpia completamente el registro de actividad"""
        self.log_text.delete("1.0", tk.END)
        self.banco.log.clear()
        self.banco.log.append("[SISTEMA] 📜 Registro limpiado")
        
        # Agregar la línea inicial
        self.log_text.insert(tk.END, "[SISTEMA] 📜 Registro limpiado\n", "sistema")
        
    def _setup_registro_actividad(self):
        """Configura el área de registro de actividad - SCROLL MANUAL"""
        log_frame = tk.Frame(self.panel3, bg='#34495e')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(log_frame, text="REGISTRO DE ACTIVIDAD", 
                font=("Arial", 12, "bold"), bg='#34495e', fg='white').pack(pady=(0, 8))

        log_text_frame = tk.Frame(log_frame, bg='#2c3e50')
        log_text_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para scrollbars
        scroll_frame = tk.Frame(log_text_frame, bg='#2c3e50')
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar VERTICAL
        v_scrollbar = tk.Scrollbar(scroll_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar HORIZONTAL  
        h_scrollbar = tk.Scrollbar(scroll_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Text widget con scroll manual
        self.log_text = tk.Text(scroll_frame, 
                            bg='#1a252f', 
                            fg='#ecf0f1',
                            yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set,
                            font=("Consolas", 8),
                            wrap=tk.NONE,  # No wrap para scroll horizontal
                            width=60,
                            height=20)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        v_scrollbar.config(command=self.log_text.yview)
        h_scrollbar.config(command=self.log_text.xview)

        # Configurar tags de colores
        self.setup_log_tags()

        # Frame para controles simples del log
        log_controls_frame = tk.Frame(log_frame, bg='#34495e')
        log_controls_frame.pack(fill=tk.X, pady=(5, 0))

        # Solo botón para limpiar (scroll siempre es manual)
        tk.Button(log_controls_frame, text="📜 Limpiar Log", 
                command=self.limpiar_log,
                font=("Arial", 8),
                bg='#7f8c8d', fg='white',
                padx=10, pady=2).pack(side=tk.LEFT)

        # 🔥 ELIMINAMOS COMPLETAMENTE EL SCROLL AUTOMÁTICO

    def setup_log_tags(self):
        """Configura los colores para el registro de actividad"""
        tags_config = {
            "entrada": "#3498db",
            "asignacion": "#27ae60", 
            "atencion": "#9b59b6",
            "prioridad": "#e67e22",
            "disponible": "#2ecc71",
            "descanso": "#95a5a6",
            "espera": "#d35400",
            "error": "#e74c3c",
            "limpieza": "#c0392b",
            "sistema": "#f1c40f",
            "notificacion": "#9b59b6"
        }
        
        for tag, color in tags_config.items():
            self.log_text.tag_configure(tag, foreground=color)

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas en tiempo real"""
        ventanillas_libres = sum(1 for v in self.banco.ventanillas if v.estado == "libre")
        en_fila = len(self.banco.fila)
        atendidos = self.banco.clientes_atendidos
        
        stats_text = (f"Ventanillas libres: {ventanillas_libres}/3\n"
                     f"Clientes en fila: {en_fila}\n"
                     f"Clientes atendidos: {atendidos}")
        
        self.stats_label.config(text=stats_text)

    def enviar_notificacion(self, cliente, ventanilla_id):
        """Envía notificación al dispositivo específico de la ventanilla"""
        dispositivo = next((disp for disp in self.dispositivos_moviles 
                          if disp['ventanilla_id'] == ventanilla_id), None)
        
        if dispositivo:
            mensaje = (f"✅ Transacción completada\nCliente: {cliente.id}\n"
                      f"Transacción: {cliente.transaccion}\nVentanilla: {ventanilla_id}\n¡Gracias!")
            
            dispositivo['notificacion'].config(text=mensaje, fg='#27ae60')
            dispositivo['estado'].config(text="🔔 Notificado", fg='#9b59b6')
            dispositivo['ultima_notificacion'] = {
                'cliente': cliente.id,
                'transaccion': cliente.transaccion,
                'timestamp': time.strftime("%H:%M:%S")
            }
            
            self.banco.log.append(f"[NOTIFICACION] Cliente {cliente.id} notificado en dispositivo {ventanilla_id}: {cliente.transaccion}")
            
            self.actualizar_estadisticas()
            
            # Limpiar notificación después de 8 segundos
            self.root.after(8000, lambda: self.limpiar_notificacion_dispositivo(ventanilla_id))
    
    def limpiar_notificacion_dispositivo(self, ventanilla_id):
        """Limpia la notificación de un dispositivo específico"""
        for disp in self.dispositivos_moviles:
            if disp['ventanilla_id'] == ventanilla_id:
                disp['notificacion'].config(text="Esperando...", fg='#7f8c8d')
                disp['estado'].config(text="🟢 Listo", fg='#27ae60')
                break

    def demo_escenario_1(self):
        """Demostración del Escenario 1: Atención con prioridad - Clientes mezclados"""
        self.reiniciar_sistema(False)  # 🔥 NO mostrar mensajes de reinicio
        self.escenario_activo = "con_prioridad"
        
        # Log de inicio
        self.banco.log.extend([
            "[DEMO] 🎭 INICIANDO ESCENARIO 1: ATENCIÓN CON PRIORIDAD",
            "        📝 Clientes normales + prioritarios en fila", 
            "        🎯 Prioritarios avanzan al frente"
        ])
        
        # Iniciar simulación
        self.simulacion_activa = True
        self.iniciar_simulacion()
        
        # Agregar clientes MEZCLADOS para el escenario 1
        tipos_clientes = [False, False, True, False]  # Normal, Normal, Prioritario, Normal
        for prioridad in tipos_clientes:
            self.banco.contador_personas += 1
            cliente = Persona(self.banco.contador_personas, prioridad)
            self.banco.agregar_persona(cliente)
        
        self.actualizar_estadisticas()
        self.actualizar_log()

    def demo_escenario_2(self):
        """Demostración del Escenario 2: Atención sin prioridad - SOLO normales"""
        self.reiniciar_sistema(False)  # 🔥 NO mostrar mensajes de reinicio
        self.escenario_activo = "sin_prioridad"
        
        # Log de inicio
        self.banco.log.extend([
            "[DEMO] 🎭 INICIANDO ESCENARIO 2: ATENCIÓN SIN PRIORIDAD",
            "        📝 Solo clientes normales en fila",
            "        🔄 Orden estricto FIFO (primero en llegar, primero en ser atendido)"
        ])
        
        # Iniciar simulación
        self.simulacion_activa = True
        self.iniciar_simulacion()
        
        # Agregar SOLO clientes NORMALES para el escenario 2
        for _ in range(4):
            self.banco.contador_personas += 1
            cliente = Persona(self.banco.contador_personas, prioridad=False)
            self.banco.agregar_persona(cliente)
        
        self.actualizar_estadisticas()
        self.actualizar_log()
    
    def demo_escenario_3(self):
        """Demostración del Escenario 3: SOLO clientes prioritarios"""
        self.reiniciar_sistema(False)  # 🔥 NO mostrar mensajes de reinicio
        self.escenario_activo = "solo_prioritarios"
        
        # Log de inicio
        self.banco.log.extend([
            "[DEMO] 🎭 INICIANDO ESCENARIO 3: SOLO CLIENTES PRIORITARIOS",
            "        👑 Todos los clientes tienen atención preferencial",
            "        🔄 Orden secuencial equitativo (todos son prioritarios)",
            "        ⚡ Asignación inmediata sin diferenciación de prioridades"
        ])
        
        # Iniciar simulación
        self.simulacion_activa = True
        self.iniciar_simulacion()
        
        # Agregar SOLO clientes PRIORITARIOS para el escenario 3
        for i in range(4):
            self.banco.contador_personas += 1
            cliente = Persona(self.banco.contador_personas, prioridad=True)
            self.banco.agregar_persona(cliente)
            self.banco.log.append(f"[PRIORIDAD] 👑 Cliente {self.banco.contador_personas} (PRIORITARIO) agregado - Todos tienen prioridad")
        
        self.actualizar_estadisticas()
        self.actualizar_log()

    def demo_escenario_4(self):
        """Demostración del Escenario 4: Todas las ventanillas ocupadas"""
        self.reiniciar_sistema(False)  # 🔥 NO mostrar mensajes de reinicio
        self.escenario_activo = "ventanillas_ocupadas"
        
        # Log de inicio
        self.banco.log.extend([
            "[DEMO] 🎭 INICIANDO ESCENARIO 4: TODAS LAS VENTANILLAS OCUPADAS",
            "        🔴 Todas las ventanillas en servicio activo",
            "        ⏳ Clientes en espera hasta que se libere una ventanilla",
            "        📊 Monitoreo constante del tiempo restante de atención",
            "        🎯 Asignación inmediata al liberarse ventanilla (prioritarios primero)"
        ])
        
        # Iniciar simulación
        self.simulacion_activa = True
        
        # Agregar clientes rápidamente para ocupar todas las ventanillas
        clientes_iniciales = []
        for i in range(3):  # Ocupar las 3 ventanillas
            self.banco.contador_personas += 1
            cliente = Persona(self.banco.contador_personas, prioridad=random.choice([True, False]))
            clientes_iniciales.append(cliente)
            self.banco.agregar_persona(cliente)
        
        # Agregar más clientes a la fila (mezcla de normales y prioritarios)
        tipos_clientes = [True, False, True, False, True]  # Mezcla para demostrar prioridad
        for prioridad in tipos_clientes:
            self.banco.contador_personas += 1
            cliente = Persona(self.banco.contador_personas, prioridad)
            self.banco.agregar_persona(cliente)
            tipo = "PRIORITARIO" if prioridad else "NORMAL"
            self.banco.log.append(f"[ESPERA] Cliente {self.banco.contador_personas} ({tipo}) en fila de espera")
        
        # Verificar estado de ventanillas
        ventanillas_ocupadas = sum(1 for v in self.banco.ventanillas if v.estado == "atendiendo")
        self.banco.log.append(f"[ESTADO] 🏦 {ventanillas_ocupadas}/3 ventanillas ocupadas - {len(self.banco.fila)} clientes en espera")
        
        if ventanillas_ocupadas == 3:
            self.banco.log.append("[MONITOREO] 🔄 Sistema monitoreando liberación de ventanillas...")
        
        self.actualizar_estadisticas()
        self.actualizar_log()
        
        # Iniciar generación automática después de 5 segundos
        self.root.after(5000, self.iniciar_simulacion)

    def iniciar_simulacion(self):
        """Inicia simulación automática"""
        if self.simulacion_activa:
            delay_llegada = random.randint(2000, 5000)
            self.root.after(delay_llegada, self.generar_persona_aleatoria)

    def generar_persona_aleatoria(self):
        """Genera cliente aleatorio - Controlado por escenario"""
        if not self.simulacion_activa:
            return
            
        self.banco.contador_personas += 1
        
        # Controlar prioridad según escenario
        if self.escenario_activo == "sin_prioridad":
            prioridad = False  # Solo normales
        elif self.escenario_activo == "solo_prioritarios":
            prioridad = True   # Solo prioritarios
        elif self.escenario_activo == "ventanillas_ocupadas":
            # Para el escenario 4, mezcla de normales y prioritarios
            prioridad = random.choice([True, False, True, False])  # 50% cada uno
        else:
            prioridad = random.choice([False, False, False, True])  # 75% normales, 25% prioritarios
        
        tipo = "PRIORITARIO" if prioridad else "NORMAL"
        self.banco.log.append(f"[GENERACION] ➕ Cliente {self.banco.contador_personas} ({tipo}) generado automáticamente")
        
        persona = Persona(self.banco.contador_personas, prioridad)
        self.banco.agregar_persona(persona)

        # Limpiar fila si es muy larga
        if len(self.banco.fila) > 30:
            self.limpiar_fila_automatica()

        self.actualizar_estadisticas()
        
        # Programar siguiente generación
        if self.simulacion_activa:
            self.root.after(random.randint(2000, 5000), self.generar_persona_aleatoria)

    def reiniciar_sistema(self, mostrar_mensajes=True):
        """Reinicia completamente el sistema para empezar desde cero
        
        Args:
            mostrar_mensajes (bool): Si muestra mensajes de reinicio o no
        """
        # Detener simulación actual
        self.simulacion_activa = False
        
        # Reiniciar banco
        self.banco.fila.clear()
        self.banco.contador_personas = 0
        self.banco.clientes_atendidos = 0
        
        # Limpiar los logs del banco
        self.banco.log.clear()
        
        # 🔥 SOLO AGREGAR MENSAJES SI SE SOLICITA EXPLÍCITAMENTE
        if mostrar_mensajes:
            self.banco.log.append("[SISTEMA] 🔄 SISTEMA REINICIADO")
            self.banco.log.append("[SISTEMA] 📊 Empezando desde Cliente 1")
            self.banco.log.append("[SISTEMA] 🏦 Sistema listo para nuevo escenario")
        
        # Liberar todas las ventanillas
        for ventanilla in self.banco.ventanillas:
            ventanilla.ocupada = False
            ventanilla.cliente = None
            ventanilla.tiempo_restante = 0
            ventanilla.estado = "libre"
        
        # Limpiar la interfaz visual de logs
        self.log_text.delete("1.0", tk.END)
        
        # Insertar los mensajes actuales en el widget de texto
        for linea in self.banco.log:
            if "[SISTEMA]" in linea:
                self.log_text.insert(tk.END, linea + "\n", "sistema")
            else:
                self.log_text.insert(tk.END, linea + "\n")
        
        # Limpiar interfaz visual
        self.limpiar_interfaz_visual()
        
        # Reiniciar escenario activo
        self.escenario_activo = None
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()

        def limpiar_fila_automatica(self):
            """Limpia la fila automáticamente cuando es muy larga"""
            if self.simulacion_activa and len(self.banco.fila) > 30:
                clientes_eliminados = len(self.banco.fila) - 15
                self.banco.fila = self.banco.fila[:15]
                self.banco.log.append(f"[SISTEMA] Fila limpiada automáticamente: {clientes_eliminados} clientes eliminados. Manteniendo 15 en fila.")
                
                # Limpiar elementos visuales
                for icon_id, texto_id, _ in self.personas_en_fila_gui[15:]:
                    self.canvas_fila.delete(icon_id)
                    self.canvas_fila.delete(texto_id)
                self.personas_en_fila_gui = self.personas_en_fila_gui[:15]
                self.actualizar_posiciones_fila()
                self.actualizar_estadisticas()

    def limpiar_interfaz_visual(self):
        """Limpia todos los elementos visuales de la interfaz"""
        # Limpiar fila visual
        for icon_id, texto_id, _ in self.personas_en_fila_gui:
            self.canvas_fila.delete(icon_id)
            self.canvas_fila.delete(texto_id)
        self.personas_en_fila_gui.clear()
        
        # Limpiar notificaciones de dispositivos móviles
        for dispositivo in self.dispositivos_moviles:
            dispositivo['notificacion'].config(text="Esperando...", fg='#7f8c8d')
            dispositivo['estado'].config(text="🟢 Listo", fg='#27ae60')
            dispositivo['ultima_notificacion'] = None
        
        # Actualizar estado de ventanillas
        self.actualizar_estado_ventanillas()
            
        # Limpiar notificaciones de dispositivos móviles
        for dispositivo in self.dispositivos_moviles:
            dispositivo['notificacion'].config(text="Esperando...", fg='#7f8c8d')
            dispositivo['estado'].config(text="🟢 Listo", fg='#27ae60')
            dispositivo['ultima_notificacion'] = None
        
        # Actualizar estado de ventanillas
        self.actualizar_estado_ventanillas()
        
        # Actualizar logs
        self.actualizar_log()

    def agregar_persona_a_fila_visual(self, persona):
        """Añade persona a la fila visual"""
        x = 50 + len(self.personas_en_fila_gui) * 45
        y = 40
        
        # Seleccionar imagen según prioridad
        imagen = self.img_prioritario if persona.prioridad else self.img_cliente
        icon_id = self.canvas_fila.create_image(x, y, image=imagen)
        
        # Crear texto con color según prioridad
        color = "red" if persona.prioridad else "black"
        texto_id = self.canvas_fila.create_text(x, y + 25, text=f"{persona.id}", 
                                              font=("Arial", 8, "bold"), fill=color)
        
        self.personas_en_fila_gui.append((icon_id, texto_id, persona))
        self.actualizar_posiciones_fila()
        self.actualizar_estadisticas()
        
        self.canvas_fila.configure(scrollregion=self.canvas_fila.bbox("all"))

    def eliminar_persona_de_fila(self, persona):
        """Elimina persona de la fila visual"""
        for i, (icon_id, texto_id, p) in enumerate(self.personas_en_fila_gui):
            if p.id == persona.id:
                self.canvas_fila.delete(icon_id)
                self.canvas_fila.delete(texto_id)
                self.personas_en_fila_gui.pop(i)
                self.actualizar_posiciones_fila()
                self.actualizar_estadisticas()
                self.canvas_fila.configure(scrollregion=self.canvas_fila.bbox("all"))
                return
        
        self.banco.log.append(f"[ERROR] No se encontró cliente {persona.id} en fila visual")

    def actualizar_posiciones_fila(self):
        """Reorganiza posiciones en la fila visual"""
        for i, (icon_id, texto_id, persona) in enumerate(self.personas_en_fila_gui):
            x = 50 + i * 45
            y = 40
            self.canvas_fila.coords(icon_id, x, y)
            self.canvas_fila.coords(texto_id, x, y + 25)

    def actualizar_estado_ventanillas(self):
        """Actualizar el estado visual de las ventanillas"""
        for vent_gui in self.ventanillas_gui:
            vent = vent_gui['ventanilla']
            
            if vent.estado == "atendiendo":
                color_estado = "#e74c3c"
                texto_estado = "ATENDIENDO"
                color_header = "#e74c3c"
            elif vent.estado == "descansando":
                color_estado = "#f39c12"
                texto_estado = "DESCANSANDO"
                color_header = "#f39c12"
            else:
                color_estado = "#27ae60"
                texto_estado = "DISPONIBLE"
                color_header = "#3498db"
            
            vent_gui['header'].configure(bg=color_header)
            for widget in vent_gui['header'].winfo_children():
                widget.configure(bg=color_header)
            
            vent_gui['estado'].configure(text=texto_estado, fg=color_estado)
            
            if vent.estado == "atendiendo" and vent.cliente:
                vent_gui['cliente'].configure(text=f"Cliente: {vent.cliente.id}")
                vent_gui['transaccion'].configure(text=f"Transacción: {vent.cliente.transaccion}")
                if vent.cliente.prioridad:
                    vent_gui['cliente'].configure(text=f"Cliente: {vent.cliente.id} (PRIORITARIO)")
                vent_gui['tiempo'].configure(text=f"Tiempo: {vent.tiempo_restante}s")
            else:
                vent_gui['cliente'].configure(text="")
                vent_gui['transaccion'].configure(text="")
                vent_gui['tiempo'].configure(text="")
        
        self.actualizar_estadisticas()

    def actualizar_log(self):
        """Actualizar el registro de actividad - SOLO AGREGAR NUEVAS LÍNEAS"""
        # Guardar posición actual del scroll ANTES de actualizar
        scroll_y_position = self.log_text.yview()[0]
        scroll_x_position = self.log_text.xview()[0]
        
        # Obtener el número actual de líneas en el widget
        lineas_actuales = int(self.log_text.index('end-1c').split('.')[0]) - 1
        
        # Solo agregar nuevas líneas si hay más en el banco.log
        if len(self.banco.log) > lineas_actuales:
            # Agregar solo las líneas nuevas
            lineas_nuevas = self.banco.log[lineas_actuales:]
            
            for linea in lineas_nuevas:
                if "[ENTRADA]" in linea:
                    tag = "entrada"
                elif "[ASIGNACION]" in linea:
                    tag = "asignacion"
                elif "[ATENCION COMPLETADA]" in linea:
                    tag = "atencion"
                elif "[PRIORIDAD]" in linea:
                    tag = "prioridad"
                elif "[DISPONIBLE]" in linea:
                    tag = "disponible"
                elif "[DESCANSO]" in linea:
                    tag = "descanso"
                elif "[ESPERA]" in linea:
                    tag = "espera"
                elif "[ERROR]" in linea:
                    tag = "error"
                elif "[LIMPIEZA]" in linea:
                    tag = "limpieza"
                elif "[SISTEMA]" in linea:
                    tag = "sistema"
                elif "[NOTIFICACION]" in linea:
                    tag = "notificacion"
                elif "[GENERACION]" in linea:
                    tag = "entrada"
                elif "[MONITOREO]" in linea:
                    tag = "sistema"
                elif "[TRANSACCION]" in linea:
                    tag = "atencion"
                elif "[ESTADO]" in linea:
                    tag = "sistema"
                elif "[DEMO]" in linea:
                    tag = "sistema"
                else:
                    tag = ""
                
                if tag:
                    self.log_text.insert(tk.END, linea + "\n", tag)
                else:
                    self.log_text.insert(tk.END, linea + "\n")
        
        # 🔥 RESTAURAR LA POSICIÓN EXACTA DEL SCROLL - SIN MOVERSE
        self.log_text.yview_moveto(scroll_y_position)
        self.log_text.xview_moveto(scroll_x_position)

    def iniciar_temporizador_ventanilla(self, ventanilla):
        """
        Inicia el temporizador para una ventanilla
        
        Args:
            ventanilla (Ventanilla): Ventanilla a monitorear
        """
        self._ejecutar_temporizador(ventanilla)
    
    def _ejecutar_temporizador(self, ventanilla):
        """Ejecuta el temporizador de la ventanilla"""
        if ventanilla.tiempo_restante > 0:
            ventanilla.tiempo_restante -= 1
            self.actualizar_estado_ventanillas()
            self.root.after(1000, lambda: self._ejecutar_temporizador(ventanilla))
        else:
            if ventanilla.estado == "atendiendo":
                self.terminar_atencion(ventanilla)
                self.iniciar_descanso_ventanilla(ventanilla)
            elif ventanilla.estado == "descansando":
                self.banco.liberar_ventanilla(ventanilla)
    
    def terminar_atencion(self, ventanilla):
        """
        Termina la atención en una ventanilla y envía notificación al dispositivo correspondiente
        """
        if ventanilla.cliente:
            self.banco.clientes_atendidos += 1
            cliente = ventanilla.cliente
            
            self.enviar_notificacion(cliente, ventanilla.id)
            
            self.banco.log.append(f"[ATENCION COMPLETADA] Cliente {cliente.id} finalizado - {cliente.transaccion}")
            cliente.estado = "atendido"
        
        ventanilla.liberar()
        self.banco.log.append(f"[DESCANSO] Ventanilla {ventanilla.id} en pausa por {ventanilla.tiempo_restante} segundos")
        self.actualizar_interfaz()
    
    def iniciar_descanso_ventanilla(self, ventanilla):
        """Inicia el temporizador de descanso para una ventanilla"""
        self._ejecutar_descanso(ventanilla)
    
    def _ejecutar_descanso(self, ventanilla):
        """Ejecuta el temporizador de descanso"""
        if ventanilla.tiempo_restante > 0:
            ventanilla.tiempo_restante -= 1
            self.actualizar_estado_ventanillas()
            self.root.after(1000, lambda: self._ejecutar_descanso(ventanilla))
        else:
            self.banco.liberar_ventanilla(ventanilla)
    
    def actualizar_interfaz(self):
        """Actualiza toda la interfaz"""
        self.actualizar_estado_ventanillas()
        self.actualizar_log()