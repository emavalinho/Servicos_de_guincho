import streamlit as st
from streamlit_folium import folium_static
import folium

PAGE_CONFIG = {"page_title":"Guinchos_de Curitiba","page_icon":":smiley:","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

def main():
	st.title("Serviços de Guincho em Curitiba")
	st.subheader("Baseado num caderno do Colab")
	menu = ["Home","Mapa de centrais de guincho"]
	choice = st.sidebar.selectbox('Menu',menu)
	if choice == 'Home':
		st.subheader("Página Inicial 1")
	elif choice == 'Mapa':
		st.subheader("Visualizar Mapa")
		with st.echo():
			m = folium.Map (location = [-25.5,-49.3],zoom_start =  11)
			folium_static(m)
	else:
		st.subheader("")
if __name__ == '__main__':
	main()
