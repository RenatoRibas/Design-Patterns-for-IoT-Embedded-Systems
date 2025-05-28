"""
Implementação do padrão Observer para monitoramento de dispositivos AI.

Define a interface Observer e uma implementação concreta (GenericSubscriber)
que reage a mudanças nos dispositivos publicados.
"""


class Observer:
    """
    Interface do Observador.
    Qualquer classe que herdar deve implementar o método `update`.
    """

    def update(self, device):
        raise NotImplementedError("O método update deve ser implementado.")


class GenericSubscriber(Observer):
    """
    Observador genérico que registra notificações de dispositivos AI.

    Attributes:
        name (str): Nome do observador.
        notifications (List[str]): Histórico de mensagens recebidas.
    """

    def __init__(self, name: str):
        self.name = name
        self.notifications = []

    def update(self, device):
        """
        Método chamado quando o dispositivo publica uma atualização.

        Args:
            device (AIDevicePublisher): Dispositivo que notificou a mudança.
        """
        if hasattr(device, "value") and device.value is not None:
            message = (
                f"Observer {self.name}: TAG = {device.tag} mudou para "
                f"{device.value} {device.unit}"
            )
        else:
            message = (
                f"Observer {self.name}: TAG = {device.tag} recebeu um valor inválido."
            )

        print(message)
        self.notifications.append(message)
