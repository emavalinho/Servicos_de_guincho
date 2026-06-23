import streamlit as st
import json
import folium

from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from folium.plugins import MeasureControl
from streamlit_folium import folium_static

# --------------------------------------------------
# Configuração da página
# --------------------------------------------------

st.set_page_config(
    page_title="Serviços de Guincho em Curitiba",
    layout="wide"
)

st.title("Serviços de Guincho em Curitiba")

# --------------------------------------------------
# Leitura dos GeoJSON
# --------------------------------------------------

with open("Divisas_de_bairros.geojson", encoding="utf-8") as f:
    bairros = json.load(f)

with open("SERVICOS_REBOQUE.geojson", encoding="utf-8") as f:
    reboque = json.load(f)

# --------------------------------------------------
# Lista de bairros
# --------------------------------------------------

lista_bairros = sorted(
    list(
        set(
            feat["properties"]["BAIRRO"]
            for feat in reboque["features"]
            if feat["properties"].get("BAIRRO")
        )
    )
)

bairro = st.sidebar.selectbox(
    "Selecione um Bairro",
    lista_bairros
)

# --------------------------------------------------
# Mapa base
# --------------------------------------------------

m = folium.Map(
    location=[-25.50, -49.30],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# --------------------------------------------------
# Bairros
# --------------------------------------------------

folium.GeoJson(
    bairros,
    name="Bairros",
    style_function=lambda x: {
        "fillColor": "#1f77b4",
        "color": "#000000",
        "weight": 1,
        "fillOpacity": 0.10
    }
).add_to(m)

# --------------------------------------------------
# Cluster
# --------------------------------------------------

cluster = MarkerCluster(
    name="Serviços de Guincho"
).add_to(m)

locations = []

# --------------------------------------------------
# Pontos filtrados por bairro
# --------------------------------------------------

for feature in reboque["features"]:

    props = feature["properties"]

    if props.get("BAIRRO") != bairro:
        continue

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

# --------------------------------------------------
# Heat Map
# --------------------------------------------------

if len(locations) > 0:

    HeatMap(
        locations,
        name="Mapa de Calor"
    ).add_to(m)

# --------------------------------------------------
# Controles
# --------------------------------------------------

folium.LayerControl().add_to(m)

m.add_child(
    MeasureControl()
)

# --------------------------------------------------
# Indicadores
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Bairro Selecionado",
        bairro
    )

with col2:
    st.metric(
        "Total de Guinchos",
        len(locations)
    )

# --------------------------------------------------
# Mapa
# --------------------------------------------------

folium_static(
    m,
    width=1200,
    height=700
)
```
