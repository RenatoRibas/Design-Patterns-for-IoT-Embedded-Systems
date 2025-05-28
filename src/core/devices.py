"""
Módulo que define os dispositivos da aplicação:
- Device (superclasse base)
- AIDevicePublisher (analógico, com padrão Observer)
- DODevice (digital, simples)
"""

from typing import List


class Device:
    """
    Superclasse para dispositivos genéricos com atributos comuns.
    """

    def __init__(self, tag: str, area: str, descricao: str, tipo: str):
        self.tag = tag
        self.area = area
        self.descricao = descricao
        self.tipo = tipo

    def __repr__(self):
        return f"Device(tag={self.tag}, area={self.area}, descricao={self.descricao}, tipo={self.tipo})"


class AIDevicePublisher(Device):
    """
    Dispositivo AI (entrada analógica) com suporte ao padrão Observer.

    Observadores podem se inscrever para receber atualizações sempre
    que o valor do sensor for modificado via update_value().
    """

    def __init__(
        self,
        tag: str,
        area: str,
        descricao: str,
        range_min: float,
        range_max: float,
        unit: str,
    ):
        super().__init__(tag, area, descricao, "AI")
        self.range_min = range_min
        self.range_max = range_max
        self.unit = unit
        self.value = None
        self.subscribers: List = []

    def subscribe(self, subscriber):
        """
        Adiciona um observador à lista de inscritos.
        """
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """
        Remove um observador da lista de inscritos.
        """
        self.subscribers.remove(subscriber)

    def notify(self):
        """
        Notifica todos os observadores inscritos.
        """
        for subscriber in self.subscribers:
            subscriber.update(self)

    def update_value(self, new_value: float):
        """
        Atualiza o valor do dispositivo e aciona os observadores.
        """
        self.value = new_value
        print(f"Atualizando {self.tag} com valor {self.value} {self.unit}")
        self.notify()

    def __repr__(self):
        return (
            f"AIDevicePublisher(tag={self.tag}, area={self.area}, descricao={self.descricao}, "
            f"range_min={self.range_min}, range_max={self.range_max}, unit={self.unit}, value={self.value})"
        )


class DODevice(Device):
    """
    Dispositivo DO (saída digital).
    """

    def __init__(self, tag: str, area: str, descricao: str):
        super().__init__(tag, area, descricao, "DO")

    def __repr__(self):
        return f"DODevice(tag={self.tag}, area={self.area}, descricao={self.descricao})"
