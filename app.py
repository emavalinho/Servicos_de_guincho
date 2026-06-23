import streamlit as st
import json
import pandas as pd
import folium

from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from folium.plugins import MeasureControl
from streamlit_folium import folium_static

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Serviços de Guincho em Curitiba",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Serviços de Guincho em Curitiba")
st.markdown("Dashboard temático por bairro")

# =====================================================
# LEITURA DOS DADOS
# =====================================================

with open("Divisas_de_bairros.geojson", encoding="utf-8") as f:
    bairros_geojson = json.load(f)

with open("SERVICOS_REBOQUE.geojson", encoding="utf-8") as f:
    reboque_geojson = json.load(f)

# =====================================================
# LISTA DE BAIRROS
# =====================================================

lista_bairros = sorted(
    list(
        set(
            feat["properties"]["BAIRRO"]
            for feat in reboque_geojson["features"]
            if feat["properties"].get("BAIRRO")
        )
    )
)

bairro = st.sidebar.selectbox(
    "Selecione um Bairro",
    lista_bairros
)

# =====================================================
# FILTRAGEM
# =====================================================

guinchos_bairro = []

for feature in reboque_geojson["features"]:

    props = feature["properties"]

    if props.get("BAIRRO") == bairro:
        guinchos_bairro.append(feature)

# =====================================================
# INDICADORES
# =====================================================

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Bairro Selecionado",
        bairro
    )

with col2:
    st.metric(
        "Quantidade de Guinchos",
        len(guinchos_bairro)
    )

# =====================================================
# MAPA
# =====================================================

m = folium.Map(
    location=[-25.50, -49.30],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# Bairros

folium.GeoJson(
    bairros_geojson,
    name="Bairros",
    style_function=lambda x: {
        "fillColor": "#4F81BD",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.15
    }
).add_to(m)

# Cluster

cluster = MarkerCluster(
    name="Serviços de Guincho"
).add_to(m)

locations = []

# Marcadores

for feature in guinchos_bairro:

    props = feature["properties"]

    coords = feature["geometry"]["coordinates"]

    lon = coords[0]
    lat = coords[1]

    nome = props.get(
        "NOME_EMPRESARIAL",
        "Sem Nome"
    )

    endereco = props.get(
        "Endereco_Completo",
        ""
    )

    popup = f"""
    <b>{nome}</b><br>
    Bairro: {bairro}<br>
    {endereco}
    """

    folium.Marker(
        location=[lat, lon],
        popup=popup,
        tooltip=nome
    ).add_to(cluster)

    locations.append(
        [lat, lon]
    )

# HeatMap

if len(locations) > 0:

    HeatMap(
        locations,
        name="Mapa de Calor"
    ).add_to(m)

# Ferramentas

folium.LayerControl().add_to(m)

m.add_child(
    MeasureControl()
)

# Exibir mapa

folium_static(
    m,
    width=1200,
    height=650
)

# =====================================================
# TABELA
# =====================================================

dados_tabela = []

for feature in guinchos_bairro:

    props = feature["properties"]

    dados_tabela.append({
        "Empresa": props.get(
            "NOME_EMPRESARIAL",
            ""
        ),
        "Bairro": props.get(
            "BAIRRO",
            ""
        ),
        "CEP": props.get(
            "CEP",
            ""
        )
    })

df = pd.DataFrame(
    dados_tabela
)

st.subheader(
    f"Empresas de Guincho - {bairro}"
)

st.dataframe(
    df,
    use_container_width=True
)
