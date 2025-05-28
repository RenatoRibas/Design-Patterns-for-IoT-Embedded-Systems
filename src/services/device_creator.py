"""
Módulo responsável por criar instâncias de dispositivos com base na entrada do tipo (DO ou AI),
aplicando os padrões de projeto Factory Method e Builder.

- DODevice: Dispositivos digitais (ex: válvulas)
- AIDevicePublisher: Dispositivos analógicos com publicação de estado (ex: sensores)
"""

import logging
from typing import Union

from src.core.builders import AIDeviceBuilder
from src.core.devices import AIDevicePublisher, DODevice
from src.core.factories import DODeviceFactory

logger = logging.getLogger(__name__)


def criar_dispositivo(tipo: str, *args) -> Union[DODevice, AIDevicePublisher]:
    """
    Cria um dispositivo com base no tipo fornecido.

    Args:
        tipo (str): Tipo do dispositivo ("DO" ou "AI").
        args: Parâmetros variáveis de acordo com o tipo:
            - DO: tag, area, descricao
            - AI: tag, area, descricao, range_min, range_max, unit

    Returns:
        Union[DODevice, AIDevicePublisher]: Instância do dispositivo criado.

    Raises:
        ValueError: Se o tipo for desconhecido.
        IndexError: Se os argumentos forem insuficientes.
    """
    if tipo == "DO":
        if len(args) < 3:
            raise IndexError("Parâmetros insuficientes para criar dispositivo DO.")
        factory = DODeviceFactory()
        dispositivo = factory.criar_device(*args[:3])
        logger.info(f"Dispositivo DO criado: {dispositivo}")
        return dispositivo

    elif tipo == "AI":
        if len(args) < 6:
            raise IndexError("Parâmetros insuficientes para criar dispositivo AI.")
        builder = (
            AIDeviceBuilder()
            .set_tag(args[0])
            .set_area(args[1])
            .set_descricao(args[2])
            .set_range_min(args[3])
            .set_range_max(args[4])
            .set_unit(args[5])
        )
        dispositivo = builder.build()
        logger.info(f"Dispositivo AI criado: {dispositivo}")
        return dispositivo

    else:
        raise ValueError(f"Tipo de dispositivo '{tipo}' desconhecido.")
