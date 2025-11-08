import random

class Persona:
    """
    Representa a un cliente en el sistema bancario
    """
    
    # Lista de transacciones posibles
    TRANSACCIONES = [
        "Retiro de efectivo",
        "Depósito de dinero",
        "Pago de servicios",
        "Consulta de saldo",
        "Transferencia bancaria",
        "Solicitud de préstamo",
        "Pago de tarjeta de crédito",
        "Apertura de cuenta",
        "Certificación financiera",
        "Cambio de moneda"
    ]
    
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
        self.transaccion = self._asignar_transaccion_aleatoria()
        self.notificacion_enviada = False
    
    def _asignar_transaccion_aleatoria(self):
        """Asigna una transacción aleatoria al cliente"""
        return random.choice(self.TRANSACCIONES)
    
    def __str__(self):
        """Representación en string de la persona"""
        tipo = "PRIORITARIO" if self.prioridad else "NORMAL"
        return f"Persona {self.id} ({tipo}) - {self.transaccion}"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Persona(id={self.id}, prioridad={self.prioridad}, transaccion={self.transaccion}, estado={self.estado})"