"""
Builder para criação de objetos AIDevicePublisher com interface fluente.
Facilita a construção passo a passo de sensores analógicos no padrão
Clean Code.
"""

from src.core.devices import AIDevicePublisher


class AIDeviceBuilder:
    """
    Builder que facilita a criação de dispositivos AI (AIDevicePublisher),
    permitindo configuração fluente dos atributos.
    """

    def __init__(self):
        self._tag: str = ""
        self._area: str = ""
        self._descricao: str = ""
        self._range_min: float = 0.0
        self._range_max: float = 100.0
        self._unit: str = ""

    def set_tag(self, tag: str) -> "AIDeviceBuilder":
        self._tag = tag
        return self

    def set_area(self, area: str) -> "AIDeviceBuilder":
        self._area = area
        return self

    def set_descricao(self, descricao: str) -> "AIDeviceBuilder":
        self._descricao = descricao
        return self

    def set_range_min(self, range_min: float) -> "AIDeviceBuilder":
        self._range_min = range_min
        return self

    def set_range_max(self, range_max: float) -> "AIDeviceBuilder":
        self._range_max = range_max
        return self

    def set_unit(self, unit: str) -> "AIDeviceBuilder":
        self._unit = unit
        return self

    def build(self) -> AIDevicePublisher:
        """
        Constrói e retorna um objeto AIDevicePublisher com os parâmetros fornecidos.
        """
        return AIDevicePublisher(
            tag=self._tag,
            area=self._area,
            descricao=self._descricao,
            range_min=self._range_min,
            range_max=self._range_max,
            unit=self._unit,
        )
