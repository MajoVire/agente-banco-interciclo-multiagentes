import tkinter as tk
import random
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
        self.root.geometry("1200x800")
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
            'light': '#ecf0f1'
        }
    
    def setup_imagenes(self):
        """Carga y configura las imágenes"""
        self.TAMANO_CLIENTE = (35, 35)
        self.TAMANO_VENTANILLA = (70, 70)
        
        try:
            self.img_cliente = ImageTk.PhotoImage(Image.open("imagenes/cliente_normal.png").resize(self.TAMANO_CLIENTE))
            self.img_prioritario = ImageTk.PhotoImage(Image.open("imagenes/cliente_prioritario.png").resize(self.TAMANO_CLIENTE))
            self.img_ventanilla = ImageTk.PhotoImage(Image.open("imagenes/ventanilla.png").resize(self.TAMANO_VENTANILLA))
        except FileNotFoundError:
            # Placeholders si no hay imágenes
            self.img_cliente = tk.PhotoImage(width=self.TAMANO_CLIENTE[0], height=self.TAMANO_CLIENTE[1])
            self.img_prioritario = tk.PhotoImage(width=self.TAMANO_CLIENTE[0], height=self.TAMANO_CLIENTE[1])
            self.img_ventanilla = tk.PhotoImage(width=self.TAMANO_VENTANILLA[0], height=self.TAMANO_VENTANILLA[1])
    
    def setup_banco(self):
        """Inicializa el sistema bancario"""
        self.banco = Banco(n_ventanillas=3, interfaz=self)
        self.personas_en_fila_gui = []
        self.simulacion_activa = True
        self.ventanillas_gui = []
    
    def setup_interfaz(self):
        """Configura todos los elementos de la interfaz gráfica"""
        self.setup_header()
        self.setup_paneles_principales()
        self.setup_ventanillas()
        self.setup_fila_clientes()
        self.setup_controles()
        self.setup_logs()
        self.setup_log_tags()
    
    def setup_header(self):
        """Configura el header de la aplicación"""
        self.header_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(self.header_frame, text="🏢 BANCO ESTRELLA", 
                font=("Arial", 20, "bold"), bg='#34495e', fg='white').pack(pady=10)
        tk.Label(self.header_frame, text="Sistema de Gestión Bancaria - Simulación Inteligente", 
                font=("Arial", 12), bg='#34495e', fg='#ecf0f1').pack(pady=(0, 10))
    
    def setup_paneles_principales(self):
        """Configura los paneles principales izquierdo y derecho"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - VENTANILLAS
        self.left_panel = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Panel derecho - CONTROLES
        self.right_panel = tk.Frame(main_frame, bg='#34495e', width=400, relief='raised', bd=2)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        self.right_panel.pack_propagate(False)
    
    def setup_ventanillas(self):
        """Configura la visualización de las ventanillas"""
        # Título ventanillas
        tk.Label(self.left_panel, text="VENTANILLAS DE ATENCIÓN", 
                font=("Arial", 14, "bold"), bg='#34495e', fg='white').pack(pady=15)

        # Frame para ventanillas
        ventanillas_frame = tk.Frame(self.left_panel, bg='#34495e')
        ventanillas_frame.pack(expand=True, pady=20)

        # Crear ventanillas visuales
        for i, vent in enumerate(self.banco.ventanillas):
            vent_frame = tk.Frame(ventanillas_frame, bg='#2c3e50', relief='solid', bd=1)
            vent_frame.pack(side=tk.LEFT, padx=25, pady=10)
            
            # Tarjeta de ventanilla
            card_frame = tk.Frame(vent_frame, bg='white', relief='raised', bd=2)
            card_frame.pack(padx=10, pady=10)
            
            # Header de ventanilla
            header_vent = tk.Frame(card_frame, bg='#3498db', height=30)
            header_vent.pack(fill=tk.X)
            header_vent.pack_propagate(False)
            
            tk.Label(header_vent, text=f"Ventanilla {vent.id}", 
                    font=("Arial", 12, "bold"), bg='#3498db', fg='white').pack(expand=True)
            
            # Contenido de ventanilla
            content_vent = tk.Frame(card_frame, bg='white', width=120, height=120)
            content_vent.pack(padx=10, pady=10)
            content_vent.pack_propagate(False)
            
            # Imagen y estado
            img_label = tk.Label(content_vent, image=self.img_ventanilla, bg='white')
            img_label.pack(pady=5)
            
            estado_label = tk.Label(content_vent, text="LIBRE", 
                                  font=("Arial", 10, "bold"), bg='white', fg='#27ae60')
            estado_label.pack()
            
            cliente_label = tk.Label(content_vent, text="", 
                                   font=("Arial", 9), bg='white', fg='#7f8c8d')
            cliente_label.pack()
            
            tiempo_label = tk.Label(content_vent, text="", 
                                  font=("Arial", 8), bg='white', fg='#e74c3c')
            tiempo_label.pack()
            
            self.ventanillas_gui.append({
                'frame': card_frame,
                'header': header_vent,
                'estado': estado_label,
                'cliente': cliente_label,
                'tiempo': tiempo_label,
                'imagen': img_label,
                'ventanilla': vent
            })
    
    def setup_fila_clientes(self):
        """Configura el área de fila de clientes"""
        fila_frame = tk.Frame(self.left_panel, bg='#34495e')
        fila_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(fila_frame, text="FILA DE CLIENTES", 
                font=("Arial", 12, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        # Canvas para fila con scroll
        fila_canvas_frame = tk.Frame(fila_frame, bg='#ecf0f1', relief='sunken', bd=2)
        fila_canvas_frame.pack(fill=tk.X, pady=5)

        self.h_scrollbar = tk.Scrollbar(fila_canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas_fila = tk.Canvas(fila_canvas_frame, height=80, bg='#ecf0f1',
                                   xscrollcommand=self.h_scrollbar.set)
        self.canvas_fila.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.h_scrollbar.config(command=self.canvas_fila.xview)

        # Leyenda de clientes
        legend_frame = tk.Frame(fila_frame, bg='#34495e')
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="Leyenda: ", font=("Arial", 9), bg='#34495e', fg='white').pack(side=tk.LEFT)
        tk.Label(legend_frame, text="● Normal", font=("Arial", 9), bg='#34495e', fg='black').pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="● Prioritario", font=("Arial", 9), bg='#34495e', fg='red').pack(side=tk.LEFT, padx=5)
    
    def setup_controles(self):
        """Configura los controles de la aplicación"""
        # ESTADÍSTICAS
        stats_frame = tk.Frame(self.right_panel, bg='#2c3e50', relief='solid', bd=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(stats_frame, text="ESTADÍSTICAS EN TIEMPO REAL", 
                font=("Arial", 12, "bold"), bg='#2c3e50', fg='white').pack(pady=10)

        self.stats_label = tk.Label(stats_frame, 
                text="Ventanillas libres: 3/3\nClientes en fila: 0\nClientes atendidos: 0\nTiempo promedio: 0s",
                font=("Arial", 10), bg='#2c3e50', fg='#ecf0f1', justify=tk.LEFT)
        self.stats_label.pack(pady=10)

        # CONTROLES
        controls_frame = tk.Frame(self.right_panel, bg='#34495e')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(controls_frame, text="CONTROLES", 
                font=("Arial", 12, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        # Botones de control (SOLO los 2 botones principales)
        button_style = {'font': ('Arial', 10), 'width': 20, 'pady': 8}

        tk.Button(controls_frame, text="➕ Agregar Cliente Normal", 
                 command=self.agregar_cliente_manual, bg='#27ae60', fg='white',
                 **button_style).pack(fill=tk.X, pady=3)

        tk.Button(controls_frame, text="🎯 Agregar Prioritario", 
                 command=self.agregar_prioritario_manual, bg='#e74c3c', fg='white',
                 **button_style).pack(fill=tk.X, pady=3)

        # Los botones de "Pausar Simulación", "Debug Fila" y "Limpiar Fila" han sido eliminados
    
    def setup_logs(self):
        """Configura el área de logs"""
        log_frame = tk.Frame(self.right_panel, bg='#34495e')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(log_frame, text="REGISTRO DE ACTIVIDAD", 
                font=("Arial", 12, "bold"), bg='#34495e', fg='white').pack(pady=(0, 10))

        # Frame para log con scroll
        log_text_frame = tk.Frame(log_frame, bg='#2c3e50')
        log_text_frame.pack(fill=tk.BOTH, expand=True)

        log_scrollbar = tk.Scrollbar(log_text_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(log_text_frame, height=15, bg='#1a252f', fg='#ecf0f1',
                               yscrollcommand=log_scrollbar.set, font=("Consolas", 9),
                               wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)
    
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

    def actualizar_estadisticas(self):
        """Actualizar las estadísticas en tiempo real"""
        ventanillas_libres = sum(1 for v in self.banco.ventanillas if v.estado == "libre")
        en_fila = len(self.banco.fila)
        atendidos = self.banco.clientes_atendidos
        
        stats_text = f"Ventanillas libres: {ventanillas_libres}/3\n"
        stats_text += f"Clientes en fila: {en_fila}\n"
        stats_text += f"Clientes atendidos: {atendidos}\n"
        stats_text += f"Tiempo promedio: {random.randint(8, 15)}s"
        
        self.stats_label.config(text=stats_text)

    # Eliminar el método limpiar_fila ya que no tenemos el botón
    # def limpiar_fila(self):

    # Eliminar el método mostrar_estado_fila ya que no tenemos el botón
    # def mostrar_estado_fila(self):

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

    # Eliminar el método toggle_simulacion ya que no tenemos el botón
    # def toggle_simulacion(self):

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

        # Auto-limpiar si la fila es muy larga (mecanismo automático)
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
            
            # Limpiar también la fila visual
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
        
        # Actualizar región de scroll
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
            
            # Actualizar header
            vent_gui['header'].configure(bg=color_header)
            for widget in vent_gui['header'].winfo_children():
                widget.configure(bg=color_header)
            
            # Actualizar estados
            vent_gui['estado'].configure(text=texto_estado, fg=color_estado)
            
            if vent.estado == "atendiendo" and vent.cliente:
                vent_gui['cliente'].configure(text=f"Cliente: {vent.cliente.id}")
                if vent.cliente.prioridad:
                    vent_gui['cliente'].configure(text=f"Cliente: {vent.cliente.id} (PRIORITARIO)")
                vent_gui['tiempo'].configure(text=f"Tiempo: {vent.tiempo_restante}s")
            else:
                vent_gui['cliente'].configure(text="")
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
                self.banco.terminar_atencion(ventanilla)
                self.iniciar_descanso_ventanilla(ventanilla)
            elif ventanilla.estado == "descansando":
                self.banco.liberar_ventanilla(ventanilla)
    
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