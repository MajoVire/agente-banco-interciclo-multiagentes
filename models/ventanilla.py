class Ventanilla:
    """
    Representa una ventanilla de atención en el banco
    """
    
    def __init__(self, id):
        """
        Inicializa una nueva ventanilla
        
        Args:
            id (int): Identificador único de la ventanilla
        """
        self.id = id
        self.ocupada = False
        self.cliente = None
        self.tiempo_restante = 0
        self.estado = "libre"  # libre, atendiendo, descansando
    
    def asignar_cliente(self, cliente, tiempo_atencion):
        """
        Asigna un cliente a la ventanilla
        
        Args:
            cliente (Persona): Cliente a atender
            tiempo_atencion (int): Tiempo de atención en segundos
        """
        self.ocupada = True
        self.estado = "atendiendo"
        self.cliente = cliente
        self.tiempo_restante = tiempo_atencion
        cliente.estado = "siendo_atendido"
    
    def liberar(self):
        """Libera la ventanilla después de atender un cliente"""
        self.ocupada = False
        self.estado = "descansando"
        self.cliente = None
        self.tiempo_restante = 3  # Tiempo de descanso
    
    def esta_libre(self):
        """Verifica si la ventanilla está disponible"""
        return self.estado == "libre"
    
    def __str__(self):
        """Representación en string de la ventanilla"""
        return f"Ventanilla {self.id} ({self.estado})"
    
    def __repr__(self):
        """Representación para debugging"""
        cliente_id = self.cliente.id if self.cliente else "None"
        return f"Ventanilla(id={self.id}, estado={self.estado}, cliente={cliente_id})"