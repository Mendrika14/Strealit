
import streamlit as st
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from joblib import Parallel, delayed
import joblib
import numpy as np
import folium
import streamlit as st
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim


""""""
def neighborhood():
    url='https://fr.wikipedia.org/wiki/Arrondissements_d%27Antananarivo'
    r = requests.get(url)
    listes=[]
    soup = BeautifulSoup(r.content, "html.parser")
    for child in soup.find_all("tbody")[0].find_all("li"):
        area=child.text.split(" ",1)[1]
        listes.append(unidecode(area))
    
    return listes



def click_button():
    st.session_state.clicked = True


st.title("Prediction house pricing !")
neighborhood_options=neighborhood()
show_map = st.checkbox("Choose neighborhood on map", value=False)

# Initialize session state to store marker location
if "marker_location" not in st.session_state:
    st.session_state.clicked = False
    st.session_state.area='Ambalavao'
    st.session_state.marker_location = [-18.9185, 47.5211]  # Default location
    st.session_state.zoom = 14  # Default zoom

m = folium.Map(location=[-18.9185, 47.5211], zoom_start=14)

m.add_child(folium.ClickForMarker())


if show_map:
    map = st_folium(m,  width=620, height=580, key="folium_map1")
    if map and map.get("last_clicked"):
        lat, lng = map["last_clicked"]["lat"], map["last_clicked"]["lng"]
        st.session_state.marker_location = [lat, lng]  # Update session state with new marker location
        st.session_state.zoom = map["zoom"]
        geolocator = Nominatim(user_agent="GetLoc")
        getLoc = geolocator.reverse(str(st.session_state.marker_location[0])+","+str(st.session_state.marker_location[1]))
        st.session_state.area=getLoc.address
        # ma = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
        # folium.Marker(
        #     location=st.session_state.marker_location,
        #     draggable=False
        # ).add_to(ma)
        # mapa = st_folium(ma, width=620, height=580, key="folium_map1")

else:
    st.session_state.area = st.selectbox("Quartier: ",
                        neighborhood_options)


area = st.number_input(label="Superficie: ",step=1)

room = st.slider("Room number: ", 1, 10)

shower_options=['Interieur', 'Exterieur']
shower = st.selectbox("Douche WC: ",
                     shower_options)

acces_options=['moto', 'voiture','voiture_parking']
acces = st.selectbox("Type d'acces: ",
                     acces_options)

furnish_options=['oui', 'non']
furnish = st.radio('Avec meuble: ',
                  furnish_options)

state_options=['bon', 'moyen','mauvais']
state = st.selectbox("Etat general: ",
                     state_options)


button=st.button('Submit',on_click=click_button)

st.text(f"Coordinates: {st.session_state.marker_location}")
st.text(f"Area: {st.session_state.area}")


if st.session_state.clicked:
    knn_from_joblib = joblib.load('model.pkl')
    test=np.array([[area,room,shower_options.index(shower),acces_options.index(acces),state_options.index(state)]])
    valeur=knn_from_joblib.predict(test)
    st.badge(str(valeur[0])+' Ar',color='green')
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(st.session_state.area)
    st.session_state.marker_location = [getLoc.latitude, getLoc.longitude]  
    st.session_state.zoom = 14  
    m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
    folium.Marker(
        location=st.session_state.marker_location,
        draggable=False
    ).add_to(m)
    map = st_folium(m, width=620, height=580, key="folium_map2")











