# Serviços de Guincho em Curitiba

Dashboard temático desenvolvido com Streamlit para visualização espacial dos serviços de guincho localizados no município de Curitiba-PR.

## Objetivo

O projeto tem como objetivo apresentar a distribuição espacial dos serviços de guincho em Curitiba por meio de um mapa interativo, permitindo a visualização dos estabelecimentos, dos bairros do município e da concentração espacial dos serviços.

## Funcionalidades

* Visualização dos bairros de Curitiba;
* Exibição dos pontos de serviços de guincho;
* Agrupamento de pontos (Marker Cluster);
* Mapa de calor (Heat Map);
* Controle de camadas;
* Ferramenta de medição de distâncias;
* Navegação interativa no mapa.

## Tecnologias Utilizadas

* Python
* Streamlit
* GeoPandas
* Folium
* Streamlit-Folium

## Estrutura do Projeto

```text
Servicos_de_guincho/

├── app.py
├── requirements.txt
├── README.md
│
└── data/
    ├── SERVICOS_REBOQUE.geojson
    └── Divisas_de_bairros.geojson
```

## Dados Utilizados

Os dados utilizados no projeto são provenientes de bases públicas disponibilizadas pelo Instituto de Pesquisa e Planejamento Urbano de Curitiba (IPPUC) e complementados por dados geoespaciais utilizados em atividades acadêmicas da disciplina.

## Como Executar Localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o aplicativo:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador.

## Publicação

O aplicativo foi desenvolvido utilizando Streamlit e pode ser publicado no Streamlit Community Cloud através da integração com o GitHub.

## Autor

Melito Júlio Avalinho

Doutorando em Ciências Geodésicas – Universidade Federal do Paraná (UFPR)
