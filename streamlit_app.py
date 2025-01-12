import folium

import streamlit as st
import pandas as pd

from streamlit_folium import st_folium
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Powerlift Anywhere", 
    page_icon=None, 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items=None,
)


st.title("Powerlifting Gyms Around the World")
st.write("Training while traveling is easy. Choose country and city to explore powerlifting gyms there")

COLUMN_WEBSITE = 'website'
COLUMN_PHONE = 'phone'
COLUMN_GOOGLE_MAP_LINK = 'Google Map Link'

df = pd.read_csv('data/gyms_powerlifting.csv', converters={COLUMN_PHONE : str})

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

COLUMNS_TO_SHOW = [
    'Gym', 'Squat rack', 'Weight Bench', 
    COLUMN_GOOGLE_MAP_LINK,
    COLUMN_WEBSITE,
    COLUMN_PHONE,
    'Country', 'City', 'Address', 
]

df = df.dropna(subset=['Gym'])

COUNTRIES = sorted(df['Country'].unique().tolist())

OPTIONS_COUNTRIES = st.multiselect(
    label="Choose country",
    options=COUNTRIES,
    default=[],
)

if len(OPTIONS_COUNTRIES) > 0:
    df = df[df['Country'].isin(OPTIONS_COUNTRIES)]

CITIES = sorted(df['City'].unique().tolist())

OPTIONS_CITIES = st.multiselect(
    label="Choose city",
    options=CITIES,
    default=[],
)

if len(OPTIONS_CITIES) > 0:
    df = df[df['City'].isin(OPTIONS_CITIES)]

N_GYMS_FOUND = len(df)
st.text(f'{N_GYMS_FOUND} gym{"s" if N_GYMS_FOUND > 1 else ""} found')

st.dataframe(
    df[COLUMNS_TO_SHOW], 
    hide_index=True, 
    width=1200,
    use_container_width=False,
    column_config={
        COLUMN_GOOGLE_MAP_LINK: st.column_config.LinkColumn(
            label=COLUMN_GOOGLE_MAP_LINK, width='medium'),
        COLUMN_WEBSITE: st.column_config.LinkColumn(
            label=COLUMN_WEBSITE, width='medium'),
    }
)

COLUMN_LATITUDE = 'latitude'
COLUMN_LONGITUDE = 'longtitude'



m = folium.Map()

def get_tooltip_text(row):
    if str(row['website']).startswith('http'):
        return f"""{row['Gym']}<br><a href=\"{row['website']}\">
{row['website']}</a><br>{row['phone']}<br>{row['Address']}"""
    else:
        return f"""{row['Gym']}<br>{row['phone']}<br>{row['Address']}"""


LATITUDES = df[COLUMN_LATITUDE].tolist()
LONGITUDES = df[COLUMN_LONGITUDE].tolist()
TOOLTIPS = df.apply(
    lambda row: get_tooltip_text(row), 
    axis=1).tolist()

for LATITUDE, LONGITUDE, TOOLTIP in zip(LATITUDES, LONGITUDES, TOOLTIPS): 
    folium.Marker(
        [LATITUDE, LONGITUDE], 
        tooltip=TOOLTIP,
        popup=TOOLTIP,
        auto_close=False,
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=1000)