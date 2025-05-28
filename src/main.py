# **************************************************
# Project: Design-Patterns-for-IoT-Embedded-Systems
# Data: 27/05/2025
# Version: 2.0
# Description:
#     Plataforma baseada em Design Patterns para integração de dispositivos IoT.
#     Leitura de dados a partir de uma planilha Excel com a lista de IOs.
#     Dispositivos instanciados via Factory Method e Builder.
#     Suporte à leitura real ou simulação com padrão Observer.
# License: MIT
# **************************************************

import logging
import os
import sys
from threading import Event, Thread

from services.io_read import read_lista_de_io
from src.services.device_creator import criar_dispositivo
from src.services.sensor_reader import ler_sensor
from src.services.sensor_simulator import loop_simulacao_sensor

# Adiciona o caminho ao src no PYTHONPATH para facilitar os imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define o modo de operação: True para sensor real, False para simulado
MODO_SENSOR = False


def main():
    """
    Função principal do sistema:
    - Lê a planilha Excel contendo a lista de IOs.
    - Valida e instancia os dispositivos via Builder e Factory.
    - Inicia a simulação ou leitura real de sensores com Observer.
    """
    # Caminho da planilha
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "..", "app", "data", "Ambiente_Controlado.xlsx")

    # Leitura da lista de IOs
    try:
        dispositivos = read_lista_de_io(file_path)
        logger.info(f"{len(dispositivos)} dispositivos lidos com sucesso.")
    except FileNotFoundError:
        logger.error("Arquivo de planilha não encontrado.")
        return
    except ValueError as e:
        logger.error(f"Erro na estrutura da planilha: {e}")
        return
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return

    # Criação dos objetos com base na planilha
    objetos_instanciados = []

    for dispositivo in dispositivos:
        try:
            tipo = dispositivo.tipo
            if tipo == "AI":
                args = [
                    dispositivo.tag,
                    dispositivo.area,
                    dispositivo.descricao,
                    dispositivo.range_min,
                    dispositivo.range_max,
                    dispositivo.unit,
                ]
            elif tipo == "DO":
                args = [
                    dispositivo.tag,
                    dispositivo.area,
                    dispositivo.descricao,
                ]
            else:
                raise ValueError(f"Tipo desconhecido: {tipo}")

            obj = criar_dispositivo(tipo, *args)
            objetos_instanciados.append(obj)

        except Exception as e:
            logger.error(f"Erro ao criar dispositivo '{dispositivo}': {e}")

    logger.info(f"{len(objetos_instanciados)} dispositivos instanciados com sucesso.")

    # Inicializa o modo de leitura (real ou simulado)
    if MODO_SENSOR:
        stop_event = Event()
        thread = Thread(
            target=ler_sensor,
            args=(objetos_instanciados, stop_event),
            daemon=True,
        )
        thread.start()
        logger.info("Leitura via sensor real iniciada.")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Encerrando leitura...")
            stop_event.set()
            thread.join()
    else:
        logger.info("Iniciando leitura simulada.")
        loop_simulacao_sensor(objetos_instanciados)


if __name__ == "__main__":
    main()
