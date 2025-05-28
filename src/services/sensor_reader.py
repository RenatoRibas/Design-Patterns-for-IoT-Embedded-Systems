"""
Módulo responsável por realizar a leitura de sensores reais via porta serial (ex: NodeMCU/ESP8266).

O valor lido é aplicado diretamente ao dispositivo correspondente, utilizando o padrão Observer.
"""

import logging
import time
from typing import List

import serial

from src.core.devices import AIDevicePublisher

logger = logging.getLogger(__name__)


def ler_sensor(dispositivos: List[AIDevicePublisher], stop_event) -> None:
    """
    Realiza a leitura contínua da porta serial e atualiza o valor do sensor real.

    Args:
        dispositivos (List[AIDevicePublisher]): Lista de dispositivos disponíveis.
        stop_event (threading.Event): Evento para encerrar a thread de leitura.
    """
    try:
        ser = serial.Serial("COM5", 115200, timeout=1)
        time.sleep(2)  # Aguarda inicialização do microcontrolador
        logger.info("Porta serial COM5 aberta com sucesso.")
    except serial.SerialException as e:
        logger.error(f"Erro ao abrir porta serial: {e}")
        return

    while not stop_event.is_set():
        try:
            if ser.in_waiting > 0:
                linha = ser.readline().decode("utf-8").strip()
                logger.debug(f"Leitura recebida: {linha}")

                if leitura_valida(linha):
                    temperatura = float(linha)

                    if not (15.0 <= temperatura <= 50.0):
                        logger.warning(
                            f"Temperatura fora do intervalo esperado: {temperatura} °C"
                        )
                        continue

                    atualizar_dispositivo(dispositivos, temperatura)
                else:
                    logger.warning(f"Formato inválido de leitura: '{linha}'")

            time.sleep(1.0)

        except Exception as e:
            logger.error(f"Erro durante leitura serial: {e}")
            break


def leitura_valida(texto: str) -> bool:
    """
    Verifica se a leitura é um valor numérico decimal válido.

    Args:
        texto (str): String lida da serial.

    Returns:
        bool: True se for número válido, False se for texto inválido ou corrompido.
    """
    return texto.replace(".", "", 1).isdigit() and texto.count(".") <= 1


def atualizar_dispositivo(
    dispositivos: List[AIDevicePublisher], temperatura: float
) -> None:
    """
    Atualiza o valor de temperatura no dispositivo identificado como 'A1-AI-TIT01'.

    Esse dispositivo representa o sensor LM35 conectado fisicamente à bancada de teste,
    cuja leitura é feita via porta serial (ex: NodeMCU ou ESP8266). A atualização
    aplica o padrão Observer, permitindo que os subscritores sejam notificados.

    Args:
        dispositivos (List[AIDevicePublisher]): Lista de dispositivos disponíveis.
        temperatura (float): Valor a ser atualizado.
    """
    for dispositivo in dispositivos:
        if dispositivo.tag == "A1-AI-TIT01":
            dispositivo.update_value(temperatura)
            logger.info(f"{dispositivo.tag} (LM35) atualizado com {temperatura} °C")
            return

    logger.warning("Dispositivo 'A1-AI-TIT01' (LM35) não encontrado para atualização.")
