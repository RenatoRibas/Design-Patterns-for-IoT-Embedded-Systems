Clean Code - Design Patterns
Visão Geral   |    Funcionalidades   |    Problemas Detectados   |    Refatoração   |    Estrutura   |    Instalação   |    Testes   |    Interface   |    CHANGELOG      

📌 Visão Geral do Projeto
Este projeto demonstra a aplicação de padrões de projeto (Design Patterns) em sistemas embarcados de IoT. Utilizando dispositivos como Raspberry Pi e ESP8266, a plataforma realiza a leitura de temperatura via comunicação serial e exibe os dados em tempo real por meio de uma interface desenvolvida em Streamlit.

O código foi estruturado com foco em reutilização, escalabilidade e legibilidade, fazendo uso de padrões como Factory Method, Builder e Observer.

🧠 Funcionalidades Principais
✅ Criação de dispositivos IoT via Factory e Builder Patterns;

✅ Leitura de dados em tempo real via serial (ESP8266);

✅ Interface interativa com Streamlit;

✅ Sistema Observer para notificação de mudanças;

✅ Estilização customizada com CSS.


## Project Structure
```
├── src/
│   ├── core/                  # Componentes centrais: padrões de projeto
│   ├── services/              # Lógica de negócios e comunicação com sensores
│   └── main.py                # Ponto de entrada do sistema
├── tests/                     # Testes unitários com pytest
├── .flake8                    # Linting com flake8
├── .pre-commit-config.yaml   # Ganchos de pre-commit
├── coverage.xml              # Relatório de cobertura
├── mkdocs.yml                # Configuração da documentação
├── pyproject.toml            # Metadados do projeto
├── requirements.txt          # Dependências do projeto
├── sonar-project.properties  # Configuração do SonarQube
├── UML.drawio                # Diagrama UML
└── README.md                 # Este arquivo

Documentação Técnica:
A documentação é gerada automaticamente utilizando MkDocs com o plugin mkdocstrings.

Instalação:
pip install mkdocs mkdocstrings[python] mkdocs-material

Executar a documentação localmente:
mkdocs serve

Acesse via navegador: http://127.0.0.1:8000

Testes e Cobertura:
Este projeto utiliza pytest e coverage para garantir a qualidade do código.

Rodar os testes com cobertura:
coverage run --source=src -m pytest
coverage xml

Trecho de exemplo do coverage.xml:
<?xml version="1.0" ?>
<coverage version="7.8.2" lines-valid="267" lines-covered="130" line-rate="0.4869">
  <sources>
    <source>C:/Users/Renato Ribas/Desktop/Engenharia de Software/Semestre 7/CleanCode/Trabalho_Intermediario/Design-Patterns-for-IoT-Embedded-Systems</source>
  </sources>
</coverage>

Análise Estática com SonarQube:
Configure o arquivo sonar-project.properties:

sonar.projectKey=Design-Patterns-for-IoT-Embedded-Systems
sonar.sources=src
sonar.python.coverage.reportPaths=coverage.xml
sonar.host.url=http://localhost:9000
sonar.token=SEU_TOKEN_AQUI

Execute o scanner:
sonar-scanner

Autor:
Renato Ribas, Jhayne Henemam

