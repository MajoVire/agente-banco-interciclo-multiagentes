import random
from models.persona import Persona
from models.ventanilla import Ventanilla

class Banco:
    """
    Sistema principal que gestiona las ventanillas y la fila de clientes
    """
    
    def __init__(self, n_ventanillas=3, interfaz=None):
        """
        Inicializa el sistema bancario
        
        Args:
            n_ventanillas (int): Número de ventanillas
            interfaz: Referencia a la interfaz gráfica
        """
        self.ventanillas = [Ventanilla(i+1) for i in range(n_ventanillas)]
        self.fila = []
        self.log = []
        self.interfaz = interfaz
        self.contador_personas = 0
        self.clientes_atendidos = 0
        
        # ✅ AGREGAR MENSAJE INICIAL ACTUALIZADO
        self.log.append("[SISTEMA] 🏦 BIENVENIDO AL SISTEMA DE GESTIÓN BANCARIA")
        self.log.append("[SISTEMA] 📋 SELECCIONE UN ESCENARIO DE DEMOSTRACIÓN:")
        self.log.append("[SISTEMA]   1. 🎭 Demo: Escenario 1 - Con prioridad")
        self.log.append("[SISTEMA]   2. 🎭 Demo: Escenario 2 - Sin prioridad") 
        self.log.append("[SISTEMA]   3. 👑 Demo: Escenario 3 - Solo prioritarios")
        self.log.append("[SISTEMA]   4. 🔴 Demo: Escenario 4 - Ventanillas ocupadas")  # NUEVA LÍNEA
        self.log.append("[SISTEMA]   ⏳ Esperando selección...")
    
    def agregar_persona(self, persona):
        """
        Agrega una persona a la fila y intenta asignarla
        
        Args:
            persona (Persona): Persona a agregar
        """
        self.fila.append(persona)
        tipo = "PRIORITARIO" if persona.prioridad else "NORMAL"
        self.log.append(f"[ENTRADA] Cliente {persona.id} ({tipo}) se une a la fila. Total en fila: {len(self.fila)}")
        
        self.actualizar_interfaz()
        if self.interfaz:
            self.interfaz.agregar_persona_a_fila_visual(persona)
        
        self.asignar()
    
    def asignar(self):
        """Asigna clientes a ventanillas libres respetando prioridades"""
        ventanillas_libres = [v for v in self.ventanillas if v.esta_libre()]
        
        if not ventanillas_libres:
            # Todas las ventanillas ocupadas - escenario 4
            if self.fila:
                ventanillas_ocupadas = len(self.ventanillas) - len(ventanillas_libres)
                prioritarios_en_espera = sum(1 for p in self.fila if p.prioridad)
                
                self.log.append(f"[ESPERA] ⏳ Todas las {ventanillas_ocupadas} ventanillas ocupadas")
                self.log.append(f"[ESPERA] 📊 {len(self.fila)} clientes esperando ({prioritarios_en_espera} prioritarios)")
                
                # Mostrar tiempos restantes de ventanillas
                for ventanilla in self.ventanillas:
                    if ventanilla.estado == "atendiendo":
                        self.log.append(f"[MONITOREO] Ventanilla {ventanilla.id}: {ventanilla.tiempo_restante}s restantes")
            return
        
        if not self.fila:
            return
        
        # Buscar cliente para asignar (prioritarios primero)
        cliente = self._obtener_siguiente_cliente()
        if cliente:
            ventanilla = ventanillas_libres[0]
            tiempo_atencion = random.randint(10, 15)
            
            self.fila.remove(cliente)
            ventanilla.asignar_cliente(cliente, tiempo_atencion)
            
            self.log.append(f"[ASIGNACION] ✅ Cliente {cliente.id} asignado a Ventanilla {ventanilla.id} - Tiempo: {tiempo_atencion}s")
            
            if self.interfaz:
                self.interfaz.eliminar_persona_de_fila(cliente)
                self.interfaz.iniciar_temporizador_ventanilla(ventanilla)
        
    def _obtener_siguiente_cliente(self):
        """
        Obtiene el siguiente cliente a atender respetando prioridades
        
        Returns:
            Persona: Siguiente cliente a atender
        """
        # Buscar clientes prioritarios primero
        prioritarios = [p for p in self.fila if p.prioridad]
        if prioritarios:
            cliente = prioritarios[0]
            self.log.append(f"[PRIORIDAD] Cliente {cliente.id} (PRIORITARIO) avanza al frente de la fila")
            return cliente
        
        # Si no hay prioritarios, tomar el primero en llegar
        return self.fila[0] if self.fila else None
    
    def terminar_atencion(self, ventanilla):
        """
        Termina la atención en una ventanilla
        
        Args:
            ventanilla (Ventanilla): Ventanilla que terminó de atender
        """
        if ventanilla.cliente:
            self.clientes_atendidos += 1
            self.log.append(f"[ATENCION COMPLETADA] ✅ Cliente {ventanilla.cliente.id} finalizado en Ventanilla {ventanilla.id}")
            self.log.append(f"[TRANSACCION] 📋 {ventanilla.cliente.transaccion} - COMPLETADA")
            ventanilla.cliente.estado = "atendido"
        
        ventanilla.liberar()
        self.log.append(f"[DESCANSO] ⏸️ Ventanilla {ventanilla.id} en pausa por {ventanilla.tiempo_restante} segundos")
        self.actualizar_interfaz()
        
    def liberar_ventanilla(self, ventanilla):
        """
        Libera completamente una ventanilla después del descanso
        
        Args:
            ventanilla (Ventanilla): Ventanilla a liberar
        """
        ventanilla.estado = "libre"
        ventanilla.tiempo_restante = 0
        
        # Verificar si hay clientes esperando
        if self.fila:
            prioritarios_esperando = sum(1 for p in self.fila if p.prioridad)
            self.log.append(f"[DISPONIBLE] 🟢 Ventanilla {ventanilla.id} LIBRE - {len(self.fila)} clientes esperando ({prioritarios_esperando} prioritarios)")
        else:
            self.log.append(f"[DISPONIBLE] 🟢 Ventanilla {ventanilla.id} LISTA - Esperando clientes")
        
        self.actualizar_interfaz()
        self.asignar()  # Intentar asignar inmediatamente
        
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas actuales del sistema
        
        Returns:
            dict: Diccionario con estadísticas
        """
        ventanillas_libres = sum(1 for v in self.ventanillas if v.esta_libre())
        en_fila = len(self.fila)
        
        return {
            'ventanillas_libres': ventanillas_libres,
            'total_ventanillas': len(self.ventanillas),
            'en_fila': en_fila,
            'atendidos': self.clientes_atendidos,
            'total_clientes': self.contador_personas
        }
    
    def actualizar_interfaz(self):
        """Actualiza la interfaz gráfica si está disponible"""
        if self.interfaz:
            self.interfaz.actualizar_estado_ventanillas()
            self.interfaz.actualizar_log()
    
    def __str__(self):
        """Representación en string del banco"""
        return f"Banco con {len(self.ventanillas)} ventanillas, {len(self.fila)} en fila"