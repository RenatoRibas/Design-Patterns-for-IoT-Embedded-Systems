##################### CLASSE CRIA OBJETO CONFORME ENTRADA ##################################################################


def criar_dispositivo(tipo, *args):
    if tipo == "DO":
        factory = DODeviceFactory()
        return factory.criar_device(*args[:3])  # tag, area, descricao
    elif tipo == "AI":
        builder = AIDeviceBuilder()
        dispositivo = (
            builder.set_tag(args[0])
            .set_area(args[1])
            .set_descricao(args[2])
            .set_range_min(args[3])
            .set_range_max(args[4])
            .set_unit(args[5])
            .build()
        )
        print(dispositivo)
        return dispositivo

    else:
        raise ValueError(f"Tipo de dispositivo {tipo} desconhecido")

    import logging


from typing import Union
from src.core.devices import DODevice, AIDevicePublisher
from src.core.factories import DODeviceFactory
from src.core.builders import AIDeviceBuilder

logger = logging.getLogger(__name__)


def criar_dispositivo(tipo: str, *args) -> Union[DODevice, AIDevicePublisher]:
    """
    Cria um dispositivo do tipo especificado (DO ou AI) com base nos parâmetros fornecidos.

    Parâmetros esperados:
        - DO: tag, area, descricao
        - AI: tag, area, descricao, range_min, range_max, unit
    """
    if tipo == "DO":
        factory = DODeviceFactory()
        return factory.criar_device(*args[:3])

    elif tipo == "AI":
        builder = AIDeviceBuilder()
        dispositivo = (
            builder.set_tag(args[0])
            .set_area(args[1])
            .set_descricao(args[2])
            .set_range_min(args[3])
            .set_range_max(args[4])
            .set_unit(args[5])
            .build()
        )
        logger.info(f"Dispositivo AI criado: {dispositivo}")
        return dispositivo

    else:
        raise ValueError(f"Tipo de dispositivo {tipo} desconhecido")
