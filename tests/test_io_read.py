import os

from src.services.io_read import AIDevice, DODevice, read_lista_de_io


def test_read_lista_de_io_ai_e_do():
    """
    Testa a função read_lista_de_io com a planilha real.

    Garante que a função retorna uma lista de dispositivos válidos
    (instâncias de DODevice ou AIDevice), com todos os campos obrigatórios preenchidos.
    """
    # Caminho absoluto para a planilha de dados
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "..", "app", "data", "Ambiente_Controlado.xlsx")

    dispositivos = read_lista_de_io(file_path)

    assert isinstance(dispositivos, list), "A função não retornou uma lista"
    assert len(dispositivos) > 0, "Lista de dispositivos está vazia"

    for dispositivo in dispositivos:
        assert isinstance(
            dispositivo, (DODevice, AIDevice)
        ), "Tipo de dispositivo inválido"
        assert dispositivo.tag, "Tag do dispositivo está vazia"
        assert dispositivo.area, "Área do dispositivo está vazia"
        assert dispositivo.descricao, "Descrição do dispositivo está vazia"

        if isinstance(dispositivo, AIDevice):
            assert isinstance(dispositivo.range_min, float), "range_min não é float"
            assert isinstance(dispositivo.range_max, float), "range_max não é float"
            assert isinstance(dispositivo.unit, str), "unit não é string"
