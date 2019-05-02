class Lote():
    def __init__(self, kg, pendiente):
        self.kg = kg
        self.pendiente = pendiente
        self.recolectado = 0


    def get_kg(self):
        return self.kg
    
    def get_pendiente(self):
        return self.pendiente