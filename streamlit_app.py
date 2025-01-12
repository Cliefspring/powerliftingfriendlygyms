import folium

import streamlit as st

from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write(
    "Add another text here!"
)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

for row in df.iloc[:1].itertuples():
    st.write(f"Gym '{row.Gym}' is located in country '{row.Country}'")


m = folium.Map(location=[df.iloc[:1]['latitude'], df.iloc[:1]['longtitude']], zoom_start=16)
for index, row in df.iloc[:1].iterrows(): 
    folium.Marker(
        [row['latitude'], row['longtitude']], 
        tooltip=row['Gym'],
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)