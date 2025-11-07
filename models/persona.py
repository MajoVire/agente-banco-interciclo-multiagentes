class Persona:
    """
    Representa a un cliente en el sistema bancario
    """
    
    def __init__(self, id, prioridad=False):
        """
        Inicializa una nueva persona
        
        Args:
            id (int): Identificador único del cliente
            prioridad (bool): Si el cliente tiene atención prioritaria
        """
        self.id = id
        self.prioridad = prioridad
        self.estado = "esperando"
    
    def __str__(self):
        """Representación en string de la persona"""
        tipo = "PRIORITARIO" if self.prioridad else "NORMAL"
        return f"Persona {self.id} ({tipo})"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Persona(id={self.id}, prioridad={self.prioridad}, estado={self.estado})"