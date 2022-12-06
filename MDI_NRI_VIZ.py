
#data processing and manipulatation
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

#visualization
import plotly.express as px
import plotly

#dashboard
import streamlit as st
st.sidebar.selectbox('Select Page', ('Home', 'Maps', 'Scatterplot', 'Bargraph'))

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df_counties = pd.read_csv("https://raw.githubusercontent.com/ellisobrien/Mapping_Environmental_Data/main/NRI_Table_Counties.csv",
                   dtype={"STCOFIPS": str})

st.title("Visualizing National Risk Index Data")
st.subheader('Ellis Obrien')
st.markdown('_Natural disasters present a fundamental risk to housing and economic security in the U.S. In 2021 Natural Disasters cost the U.S $145 Billion. In an effort to improve data surrounding natural disasters the Federal Emergency Management Agency released the National Risk Index which provides comprehensive county level data on natural disaster risks._')

df_state=df_counties.groupby('STATEABBRV').agg({'EAL_VALT':'sum', 'POPULATION':'sum', 'RISK_SCORE':'mean'})
df_state['STATE'] = df_state.index
df_state['per_cap_loss'] = df_state.EAL_VALT.div(df_state.POPULATION)

st.subheader('State Level Loss')
st.write('It will be important for policy makers to understand geographic losses. Visualizing losses at the state level give us a high level sense of underlying risk.')

fig1 = px.choropleth(df_state, locations='STATE', color='per_cap_loss',
                               color_continuous_scale='balance',
                               locationmode="USA-states",
                               labels={'EAL_VALT':'Expected Annual Loss', 'STCOFIPS':'FIPS'},
                              )
fig1.update_layout(title_text = '<b>Risk Score by State</b> <br><sup>West Coast and Tornado Alley Have Highest Per Capita Loss</sup>',title_y=0.8, title_x=0.75, geo_scope='usa')
st.plotly_chart(fig1)

st.subheader('Mapping County Level Data')
st.write('Understanding more granular risk can give us a better since of what is driving losses in the map above.')


map_list=list(df_counties.columns)
map_array = np.array(map_list)
index = [0, 1, 2, 3, 4, 5, 6,
       7, 8]
map_array = np.delete(map_array, index)


#Enter Variables to Map here
answer2=st.selectbox(label="What variable would you like to Map?",
options=(map_array))


#Enter Variable Description
NRI_description='Composite Risk Score'

#Enter Bin Range Here
Map_Range=(0,40)

#initilizing mapping function
def county_map(input_var):
    fig2 = px.choropleth_mapbox(df_counties,geojson=counties, locations='STCOFIPS', color=input_var,
                               color_continuous_scale="balance",
                               range_color=Map_Range,
                               mapbox_style="carto-positron",
                               zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               labels={input_var:input_var, 'STCOFIPS':'FIPS'}
                              )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
    st.plotly_chart(fig2)

#running mapping function
county_map(answer2)

st.subheader('Relationships Between Data')
st.write('Viewing Relationships for National Risk Index Data.')


#Enter X variable and Description
answer_3x=st.selectbox(label="What variable would you like as an X-Value?",
options=(map_array))

#Enter Y Variable and Description
answer_3y=st.selectbox(label="What variable would you like as a Y-Value?",
options=(map_array))


def scatter_plot(x_value, y_value):
    fig3= px.scatter(df_counties, x=x_value, y=y_value,
                     size="POPULATION",
                     size_max=15,
                     template="simple_white")

    st.plotly_chart(fig3)

scatter_plot(answer_3x, answer_3y)


#running function
