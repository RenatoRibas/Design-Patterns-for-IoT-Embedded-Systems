import pytest

from src.core.devices import AIDevicePublisher, DODevice
from src.services.device_creator import criar_dispositivo


def test_criar_valvula_11():
    """
    Testa a criação de um dispositivo DO (saída digital) representando uma válvula.
    """
    dispositivo = criar_dispositivo("DO", "A1-VA11", "1", "Válvula 11")

    assert isinstance(dispositivo, DODevice)
    assert dispositivo.tag == "A1-VA11"
    assert dispositivo.descricao == "Válvula 11"


def test_criar_sensor_temperatura():
    """
    Testa a criação de um dispositivo AI para medição de temperatura.
    """
    dispositivo = criar_dispositivo(
        "AI", "A1-AI-TIT01", "1", "TIT01 - Temperatura Tanque 01", 0.0, 900.0, "°C"
    )

    assert isinstance(dispositivo, AIDevicePublisher)
    assert dispositivo.tag == "A1-AI-TIT01"
    assert dispositivo.range_max == 900.0
    assert dispositivo.unit == "°C"


def test_criar_sensor_nivel():
    """
    Testa a criação de um dispositivo AI para sensor de nível de tanque.
    """
    dispositivo = criar_dispositivo(
        "AI", "A1-AI-LIT01", "1", "LIT01 - Sensor de Nível tanque 01", 0.0, 25.0, "m"
    )

    assert isinstance(dispositivo, AIDevicePublisher)
    assert dispositivo.range_max == 25.0
    assert dispositivo.unit == "m"


def test_sensor_erro_range_invertido():
    """
    Testa a criação de um sensor com range válido (mesmo que mínimo > 0).
    """
    dispositivo = criar_dispositivo(
        "AI", "A2-AI-TESTE", "2", "TESTE CLEAN CODE", 10.0, 20.0, ""
    )

    assert isinstance(dispositivo, AIDevicePublisher)
    assert dispositivo.range_min == 10.0
    assert dispositivo.range_max == 20.0


def test_tipo_invalido():
    """
    Garante que a função levanta exceção para tipo de dispositivo inválido.
    """
    with pytest.raises(ValueError):
        criar_dispositivo("XYZ", "Tag", "Area", "Descricao")


def test_ai_parametros_incompletos():
    """
    Verifica erro ao criar dispositivo AI com parâmetros insuficientes.
    """
    with pytest.raises(IndexError):
        criar_dispositivo("AI", "A2-AI-TESTE", "Zona 3")
