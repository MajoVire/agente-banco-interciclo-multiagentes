import tkinter as tk
import random
import time
from PIL import Image, ImageTk

from models.banco import Banco
from models.persona import Persona

class InterfazBanco:
    """
    Interfaz gráfica para el sistema de gestión bancaria
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica
        
        Args:
            root (tk.Tk): Ventana principal de Tkinter
        """
        self.root = root
        self.setup_ventana_principal()
        self.setup_estilos()
        self.setup_imagenes()
        self.setup_banco()
        self.setup_interfaz()
        self.iniciar_simulacion()
    
    def setup_ventana_principal(self):
        """Configura la ventana principal"""
        self.root.title("Sistema de Gestión Bancaria - Simulación Inteligente")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
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
        self.TAMANO_CLIENTE = (30, 30)
        self.TAMANO_PRIORITARIO = (30,30)
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
                imagen = Image.open(ruta)
                imagen_redimensionada = imagen.resize(
                    getattr(self, f'TAMANO_{nombre.upper()}') 
                    if nombre != 'celular' else self.TAMANO_CELULAR
                )
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
        colores = {
            'cliente': '#3498db',      # Azul
            'prioritario': '#e74c3c',  # Rojo
            'ventanilla': '#27ae60',   # Verde
            'celular': '#9b59b6'       # Púrpura
        }
        
        color = colores.get(tipo_imagen, '#95a5a6')
        
        if tipo_imagen == 'celular':
            tamaño = self.TAMANO_CELULAR
        else:
            tamaño = self.TAMANO_CLIENTE
        
        # Crear imagen de color sólido
        imagen = Image.new('RGB', tamaño, color)
        
        # Agregar texto identificador
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(imagen)
        
        try:
            # Intentar usar una fuente más pequeña
            font = ImageFont.load_default()
            texto = tipo_imagen.upper()[:3]
            draw.text((tamaño[0]//2, tamaño[1]//2), texto, fill='white', anchor='mm', font=font)
        except:
            pass
        
        imagen_tk = ImageTk.PhotoImage(imagen)
        setattr(self, f'img_{tipo_imagen}', imagen_tk)
        print(f"🔄 Placeholder creado para {tipo_imagen}")
    
    def setup_banco(self):
        """Inicializa el sistema bancario"""
        self.banco = Banco(n_ventanillas=3, interfaz=self)
        self.personas_en_fila_gui = []
        self.simulacion_activa = True
        self.ventanillas_gui = []
        self.dispositivos_moviles = []
    
    def setup_interfaz(self):
        """Configura todos los elementos de la interfaz gráfica"""
        self.setup_header()
        self.setup_paneles_principales()
        self.setup_panel1_ventanillas()
        self.setup_panel2_fila_notificaciones()
        self.setup_panel3_estadisticas_controles()
        self.setup_logs()
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
        """Configura los paneles principales según la nueva estructura"""
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # PANEL 1: Ventanillas de atención (izquierda)
        self.panel1 = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2, width=400)
        self.panel1.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        self.panel1.pack_propagate(False)

        # PANEL 2: Fila de clientes + Notificaciones (centro)
        self.panel2 = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        self.panel2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # PANEL 3: Estadísticas + Controles (derecha)
        self.panel3 = tk.Frame(main_frame, bg='#34495e', width=400, relief='raised', bd=2)
        self.panel3.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.panel3.pack_propagate(False)
    
    def setup_panel1_ventanillas(self):
        """Configura el PANEL 1: Ventanillas de atención"""
        tk.Label(self.panel1, text="VENTANILLAS DE ATENCIÓN", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=15)

        ventanillas_frame = tk.Frame(self.panel1, bg='#34495e')
        ventanillas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for i, vent in enumerate(self.banco.ventanillas):
            vent_frame = tk.Frame(ventanillas_frame, bg='#2c3e50', relief='solid', bd=1)
            vent_frame.pack(fill=tk.X, padx=10, pady=10)
            
            card_frame = tk.Frame(vent_frame, bg='white', relief='raised', bd=2)
            card_frame.pack(fill=tk.X, padx=8, pady=8)
            
            header_vent = tk.Frame(card_frame, bg='#3498db', height=30)
            header_vent.pack(fill=tk.X)
            header_vent.pack_propagate(False)
            
            tk.Label(header_vent, text=f"Ventanilla {vent.id}", 
                    font=("Arial", 12, "bold"), bg='#3498db', fg='white').pack(expand=True)
            
            content_vent = tk.Frame(card_frame, bg='white', height=100)
            content_vent.pack(fill=tk.X, padx=8, pady=8)
            content_vent.pack_propagate(False)
            
            img_frame = tk.Frame(content_vent, bg='white', width=80)
            img_frame.pack(side=tk.LEFT, fill=tk.Y)
            img_frame.pack_propagate(False)
            
            img_label = tk.Label(img_frame, image=self.img_ventanilla, bg='white')
            img_label.pack(expand=True, padx=5)
            
            info_frame = tk.Frame(content_vent, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))
            
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
            
            self.ventanillas_gui.append({
                'frame': card_frame,
                'header': header_vent,
                'estado': estado_label,
                'cliente': cliente_label,
                'transaccion': transaccion_label,
                'tiempo': tiempo_label,
                'imagen': img_label,
                'ventanilla': vent
            })
    
    def setup_panel2_fila_notificaciones(self):
        """Configura el PANEL 2: Fila de clientes + Notificaciones móviles"""
        
        # Sección FILA DE CLIENTES
        fila_frame = tk.Frame(self.panel2, bg='#34495e')
        fila_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(fila_frame, text="FILA DE CLIENTES", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        fila_canvas_frame = tk.Frame(fila_frame, bg='#ecf0f1', relief='sunken', bd=2)
        fila_canvas_frame.pack(fill=tk.X, pady=5)

        self.h_scrollbar = tk.Scrollbar(fila_canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas_fila = tk.Canvas(fila_canvas_frame, height=80, bg='#ecf0f1',
                                   xscrollcommand=self.h_scrollbar.set)
        self.canvas_fila.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.h_scrollbar.config(command=self.canvas_fila.xview)

        legend_frame = tk.Frame(fila_frame, bg='#34495e')
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="Leyenda: ", font=("Arial", 9), bg='#34495e', fg='white').pack(side=tk.LEFT)
        tk.Label(legend_frame, text="● Normal", font=("Arial", 9), bg='#34495e', fg='black').pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="● Prioritario", font=("Arial", 9), bg='#34495e', fg='red').pack(side=tk.LEFT, padx=5)

        # Separador
        separator = tk.Frame(self.panel2, height=2, bg='#7f8c8d')
        separator.pack(fill=tk.X, padx=20, pady=10)

        # Sección NOTIFICACIONES MÓVILES
        notif_frame = tk.Frame(self.panel2, bg='#34495e')
        notif_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(notif_frame, text="📱 NOTIFICACIONES MÓVILES POR VENTANILLA", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        dispositivos_frame = tk.Frame(notif_frame, bg='#34495e')
        dispositivos_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.dispositivos_moviles = []
        for i in range(3):
            dispositivo_frame = tk.Frame(dispositivos_frame, bg='#34495e')
            dispositivo_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=8)
            
            tk.Label(dispositivo_frame, text=f"Ventanilla {i+1}", 
                    font=("Arial", 11, "bold"), bg='#34495e', fg='white').pack(pady=(0, 8))
            
            celular_frame = tk.Frame(dispositivo_frame, bg='#1a1a1a', relief='sunken', bd=3, 
                                   width=160, height=240)
            celular_frame.pack(pady=5)
            celular_frame.pack_propagate(False)

            celular_display = tk.Frame(celular_frame, bg='#2c3e50')
            celular_display.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

            notif_celular_frame = tk.Frame(celular_display, bg='#ecf0f1')
            notif_celular_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            notificacion_label = tk.Label(notif_celular_frame, 
                                        text="Esperando...",
                                        font=("Arial", 9),
                                        bg='#ecf0f1', fg='#7f8c8d',
                                        wraplength=130,
                                        justify=tk.LEFT)
            notificacion_label.pack(expand=True, padx=5, pady=5)

            estado_label = tk.Label(dispositivo_frame, text="🟢 Listo",
                                  font=("Arial", 9),
                                  bg='#34495e', fg='#27ae60')
            estado_label.pack(pady=5)

            self.dispositivos_moviles.append({
                'frame': dispositivo_frame,
                'celular': celular_frame,
                'notificacion': notificacion_label,
                'estado': estado_label,
                'ventanilla_id': i + 1,
                'ultima_notificacion': None
            })

        self.contador_notif_frame = tk.Frame(notif_frame, bg='#34495e')
        self.contador_notif_frame.pack(fill=tk.X, pady=10)
    
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
        controls_frame = tk.Frame(self.panel3, bg='#34495e')
        controls_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(controls_frame, text="CONTROLES", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 15))

        button_style = {'font': ('Arial', 11), 'width': 22, 'pady': 10}

        tk.Button(controls_frame, text="➕ Agregar Cliente Normal", 
                 command=self.agregar_cliente_manual, bg='#27ae60', fg='white',
                 **button_style).pack(fill=tk.X, pady=8)

        tk.Button(controls_frame, text="🎯 Agregar Prioritario", 
                 command=self.agregar_prioritario_manual, bg='#e74c3c', fg='white',
                 **button_style).pack(fill=tk.X, pady=8)

        # Separador para el registro de actividad
        separator2 = tk.Frame(self.panel3, height=2, bg='#7f8c8d')
        separator2.pack(fill=tk.X, padx=20, pady=15)

        # Sección REGISTRO DE ACTIVIDAD en el panel 3
        log_frame = tk.Frame(self.panel3, bg='#34495e')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(log_frame, text="REGISTRO DE ACTIVIDAD", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        log_text_frame = tk.Frame(log_frame, bg='#2c3e50')
        log_text_frame.pack(fill=tk.BOTH, expand=True)

        log_scrollbar = tk.Scrollbar(log_text_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(log_text_frame, height=15, bg='#1a252f', fg='#ecf0f1',
                               yscrollcommand=log_scrollbar.set, font=("Consolas", 8),
                               wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)

    def setup_logs(self):
        """Configura el área de logs (ya está en setup_panel3_estadisticas_controles)"""
        pass
    
    def setup_log_tags(self):
        """Configura los colores para el registro de actividad"""
        self.log_text.tag_configure("entrada", foreground="#3498db")
        self.log_text.tag_configure("asignacion", foreground="#27ae60")
        self.log_text.tag_configure("atencion", foreground="#9b59b6")
        self.log_text.tag_configure("prioridad", foreground="#e67e22")
        self.log_text.tag_configure("disponible", foreground="#2ecc71")
        self.log_text.tag_configure("descanso", foreground="#95a5a6")
        self.log_text.tag_configure("espera", foreground="#d35400")
        self.log_text.tag_configure("error", foreground="#e74c3c")
        self.log_text.tag_configure("limpieza", foreground="#c0392b")
        self.log_text.tag_configure("sistema", foreground="#f1c40f")
        self.log_text.tag_configure("notificacion", foreground="#9b59b6")

    # Los métodos restantes se mantienen igual...
    def actualizar_estadisticas(self):
        """Actualizar las estadísticas en tiempo real"""
        ventanillas_libres = sum(1 for v in self.banco.ventanillas if v.estado == "libre")
        en_fila = len(self.banco.fila)
        atendidos = self.banco.clientes_atendidos
        
        stats_text = f"Ventanillas libres: {ventanillas_libres}/3\n"
        stats_text += f"Clientes en fila: {en_fila}\n"
        stats_text += f"Clientes atendidos: {atendidos}\n"
        
        
        self.stats_label.config(text=stats_text)
      

    def enviar_notificacion(self, cliente, ventanilla_id):
        """Envía notificación al dispositivo específico de la ventanilla"""
        dispositivo = None
        for disp in self.dispositivos_moviles:
            if disp['ventanilla_id'] == ventanilla_id:
                dispositivo = disp
                break
        
        if dispositivo:
            mensaje = f"✅ Transacción completada\nCliente: {cliente.id}\nTransacción: {cliente.transaccion}\nVentanilla: {ventanilla_id}\n¡Gracias!"
            
            dispositivo['notificacion'].config(text=mensaje, fg='#27ae60')
            dispositivo['estado'].config(text="🔔 Notificado", fg='#9b59b6')
            dispositivo['ultima_notificacion'] = {
                'cliente': cliente.id,
                'transaccion': cliente.transaccion,
                'timestamp': time.strftime("%H:%M:%S")
            }
            
            self.banco.log.append(f"[NOTIFICACION] Cliente {cliente.id} notificado en dispositivo {ventanilla_id}: {cliente.transaccion}")
            
            self.actualizar_estadisticas()
            
            self.root.after(8000, lambda: self.limpiar_notificacion_dispositivo(ventanilla_id))
    
    def limpiar_notificacion_dispositivo(self, ventanilla_id):
        """Limpia la notificación de un dispositivo específico"""
        for disp in self.dispositivos_moviles:
            if disp['ventanilla_id'] == ventanilla_id:
                disp['notificacion'].config(text="Esperando...", fg='#7f8c8d')
                disp['estado'].config(text="🟢 Listo", fg='#27ae60')
                break

    def agregar_cliente_manual(self):
        """Agregar cliente normal manualmente"""
        self.banco.contador_personas += 1
        persona = Persona(self.banco.contador_personas, prioridad=False)
        self.banco.agregar_persona(persona)
        self.actualizar_estadisticas()

    def agregar_prioritario_manual(self):
        """Agregar cliente prioritario manualmente"""
        self.banco.contador_personas += 1
        persona = Persona(self.banco.contador_personas, prioridad=True)
        self.banco.agregar_persona(persona)
        self.actualizar_estadisticas()

    def iniciar_simulacion(self):
        """Iniciar simulación automática"""
        if not self.simulacion_activa:
            return
        delay_llegada = random.randint(2000, 5000)
        self.root.after(delay_llegada, self.generar_persona_aleatoria)

    def generar_persona_aleatoria(self):
        """Generar cliente aleatorio"""
        if not self.simulacion_activa:
            return
        self.banco.contador_personas += 1
        prioridad = random.choice([False, False, False, True])
        persona = Persona(self.banco.contador_personas, prioridad)
        self.banco.agregar_persona(persona)

        if len(self.banco.fila) > 30:
            self.limpiar_fila_automatica()

        self.actualizar_estadisticas()
        self.root.after(random.randint(2000, 5000), self.generar_persona_aleatoria)

    def limpiar_fila_automatica(self):
        """Limpia la fila automáticamente cuando es muy larga"""
        if len(self.banco.fila) > 30:
            clientes_eliminados = len(self.banco.fila) - 15
            self.banco.fila = self.banco.fila[:15]
            self.banco.log.append(f"[SISTEMA] Fila limpiada automáticamente: {clientes_eliminados} clientes eliminados. Manteniendo 15 en fila.")
            
            for icon_id, texto_id, _ in self.personas_en_fila_gui[15:]:
                self.canvas_fila.delete(icon_id)
                self.canvas_fila.delete(texto_id)
            self.personas_en_fila_gui = self.personas_en_fila_gui[:15]
            self.actualizar_posiciones_fila()
            self.actualizar_estadisticas()

    def agregar_persona_a_fila_visual(self, persona):
        """Añadir persona a la fila visual"""
        x = 50 + len(self.personas_en_fila_gui) * 45
        y = 40
        
        imagen = self.img_prioritario if persona.prioridad else self.img_cliente
        icon_id = self.canvas_fila.create_image(x, y, image=imagen)
        
        color = "red" if persona.prioridad else "black"
        texto_id = self.canvas_fila.create_text(x, y + 25, text=f"{persona.id}", 
                                              font=("Arial", 8, "bold"), fill=color)
        
        self.personas_en_fila_gui.append((icon_id, texto_id, persona))
        self.actualizar_posiciones_fila()
        self.actualizar_estadisticas()
        
        self.canvas_fila.configure(scrollregion=self.canvas_fila.bbox("all"))

    def eliminar_persona_de_fila(self, persona):
        """Eliminar persona de la fila visual"""
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
        """Reorganizar posiciones en la fila visual"""
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
        """Actualizar el registro de actividad"""
        self.log_text.delete("1.0", tk.END)
        for linea in self.banco.log[-20:]:
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
            else:
                tag = ""
            
            if tag:
                self.log_text.insert(tk.END, linea + "\n", tag)
            else:
                self.log_text.insert(tk.END, linea + "\n")
        
        self.log_text.see(tk.END)

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