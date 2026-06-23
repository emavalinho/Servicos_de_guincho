import streamlit as st
import geopandas as gpd
import folium

from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from folium.plugins import MeasureControl
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Serviços de Guincho em Curitiba",
    layout="wide"
)

st.title("Serviços de Guincho em Curitiba")

# leitura dos dados
bairros = gpd.read_file(
    "data/Divisas_de_bairros.geojson"
)

reboque = gpd.read_file(
    "data/SERVICOS_REBOQUE.geojson"
)

# mapa base
m = folium.Map(
    location=[-25.5, -49.3],
    zoom_start=12
)

# bairros
folium.GeoJson(
    bairros,
    name="Bairros"
).add_to(m)

# cluster
cluster = MarkerCluster(
    name="Guinchos"
).add_to(m)

for idx, row in reboque.iterrows():

    folium.Marker(
        [
            row.geometry.y,
            row.geometry.x
        ]
    ).add_to(cluster)

# heatmap
locations = []

for idx, row in reboque.iterrows():

    locations.append(
        [
            row.geometry.y,
            row.geometry.x
        ]
    )

HeatMap(
    locations,
    name="Mapa de Calor"
).add_to(m)

# controle
folium.LayerControl().add_to(m)

# medição
m.add_child(
    MeasureControl()
)

folium_static(
    m,
    width=1200,
    height=700
)

st.metric(
    "Total de Guinchos",
    len(reboque)
)
