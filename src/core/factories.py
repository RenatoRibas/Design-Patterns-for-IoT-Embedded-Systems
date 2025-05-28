"""
Factory responsável pela criação de dispositivos digitais (DODevice),
seguindo o padrão Factory Method.
"""

from src.core.devices import DODevice


class DODeviceFactory:
    """
    Fábrica para instanciar objetos DODevice.
    Encapsula o processo de criação de dispositivos digitais.
    """

    def criar_device(self, tag: str, area: str, descricao: str) -> DODevice:
        """
        Cria e retorna um objeto DODevice.

        Args:
            tag (str): Identificador do dispositivo.
            area (str): Área de localização.
            descricao (str): Descrição funcional.

        Returns:
            DODevice: Instância criada com os dados fornecidos.
        """
        return DODevice(tag, area, descricao)
