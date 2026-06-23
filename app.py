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
# ESTATÍSTICAS DOS BAIRROS
# =====================================================

estatisticas = []

for bairro_feature in bairros_geojson["features"]:

    props = bairro_feature["properties"]

    nome_bairro = props.get("NOME")

    area_m2 = props.get("SHAPE_AREA", 0)

    quantidade = 0

    for guincho in reboque_geojson["features"]:

        if guincho["properties"].get("BAIRRO") == nome_bairro:
            quantidade += 1

    area_km2 = area_m2 / 1000000

    densidade = 0

    if area_km2 > 0:
        densidade = quantidade / area_km2

    estatisticas.append({
        "BAIRRO": nome_bairro,
        "AREA_KM2": round(area_km2, 2),
        "GUINCHOS": quantidade,
        "DENSIDADE": round(densidade, 2)
    })

df_estatisticas = pd.DataFrame(estatisticas)

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

bairro_info = df_estatisticas[
    df_estatisticas["BAIRRO"] == bairro
].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Bairro",
        bairro
    )

with col2:
    st.metric(
        "Área (km²)",
        bairro_info["AREA_KM2"]
    )

with col3:
    st.metric(
        "Guinchos",
        bairro_info["GUINCHOS"]
    )

with col4:
    st.metric(
        "Guinchos/km²",
        bairro_info["DENSIDADE"]
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

st.subheader("Quantidade de Guinchos por Bairro")

ranking = df_estatisticas.sort_values(
    "GUINCHOS",
    ascending=False
)

st.bar_chart(
    ranking.set_index("BAIRRO")["GUINCHOS"]
)

st.subheader("Área do Bairro x Quantidade de Guinchos")

grafico_disp = df_estatisticas[
    ["BAIRRO", "AREA_KM2", "GUINCHOS"]
]

st.scatter_chart(
    grafico_disp,
    x="AREA_KM2",
    y="GUINCHOS"
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
