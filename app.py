import streamlit as st
import json
import folium

from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from folium.plugins import MeasureControl
from streamlit_folium import folium_static

# Configuração da página
st.set_page_config(
    page_title="Serviços de Guincho em Curitiba",
    layout="wide"
)

st.title("Serviços de Guincho em Curitiba")

# Leitura dos GeoJSON
with open("data/Divisas_de_bairros.geojson", encoding="utf-8") as f:
    bairros = json.load(f)

with open("data/SERVICOS_REBOQUE.geojson", encoding="utf-8") as f:
    reboque = json.load(f)

# Mapa base
m = folium.Map(
    location=[-25.5, -49.3],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# Camada dos bairros
folium.GeoJson(
    bairros,
    name="Bairros"
).add_to(m)

# Cluster de guinchos
cluster = MarkerCluster(
    name="Guinchos"
).add_to(m)

locations = []

# Percorre os pontos do GeoJSON
for feature in reboque["features"]:

    geom = feature["geometry"]

    if geom["type"] == "Point":

        lon, lat = geom["coordinates"]

        folium.Marker(
            [lat, lon]
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

# Controle de camadas
folium.LayerControl().add_to(m)

# Ferramenta de medição
m.add_child(
    MeasureControl()
)

# Exibição do mapa
folium_static(
    m,
    width=1200,
    height=700
)

# Indicador
st.metric(
    "Total de Guinchos",
    len(locations)
)
