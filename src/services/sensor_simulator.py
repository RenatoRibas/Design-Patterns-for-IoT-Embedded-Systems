"""
Módulo responsável por simular a leitura de temperatura de um sensor AI (ex: LM35)
em ambientes onde a leitura via hardware real (ex: NodeMCU) não está disponível.

A simulação aplica os valores diretamente ao dispositivo 'A1-AI-TIT01', utilizando o padrão Observer.
"""

import logging
import random
import time
from typing import List

from src.core.devices import AIDevicePublisher

logger = logging.getLogger(__name__)


def simular_sensor_temperatura() -> float:
    """
    Gera um valor de temperatura simulado.

    Simula um sensor do tipo LM35 com leitura entre 15°C e 35°C,
    com precisão de duas casas decimais.

    Returns:
        float: Valor de temperatura simulado.
    """
    return round(random.uniform(15.0, 35.0), 2)


def loop_simulacao_sensor(
    dispositivos: List[AIDevicePublisher], intervalo: float = 1.0
) -> None:
    """
    Loop contínuo de simulação da leitura de sensores AI.

    Para cada iteração, simula um valor de temperatura e atualiza
    o dispositivo identificado como 'A1-AI-TIT01' — que representa
    o sensor LM35 da bancada de teste.

    Args:
        dispositivos (List[AIDevicePublisher]): Lista de dispositivos instanciados.
        intervalo (float): Intervalo entre simulações, em segundos.
    """
    while True:
        temperatura = simular_sensor_temperatura()
        logger.info(f"Simulação: temperatura lida = {temperatura} °C")

        for dispositivo in dispositivos:
            if dispositivo.tag == "A1-AI-TIT01":
                dispositivo.update_value(temperatura)
                logger.info(
                    f"{dispositivo.tag} (LM35 simulado) atualizado com {temperatura} °C"
                )

        time.sleep(intervalo)
