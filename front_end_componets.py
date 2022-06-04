from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd 
import pyproj
import plotly.graph_objects as go

#app-------------------------------------------------------------------------------------
app = Dash(__name__)
#--------------------------------------------------------------------------------------------------------------




#MAPA derecha
map_df = gpd.read_file('data/2006.geojson')
# map_df = map_df.to_crs(epsg=4326)
# map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
# map_df = map_df.set_index('grilla1')
# map_df = map_df.sample(100)
# join the geodataframe with the cleaned up csv dataframe
#merged = merged.reset_index()

map_df["x"] = map_df.representative_point().x
map_df["y"] = map_df.representative_point().y

# fig = px.choropleth(map_df, geojson=map_df.geometry, locations=map_df.index, color="areacoca")
# fig.update_geos(fitbounds="locations", visible=False)
map_df = map_df.sample(100)
fig = go.Figure(go.Densitymapbox(lat=map_df.y, lon=map_df.x, z=map_df.areacoca,
                                 radius=10))
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
fig.update_layout(
        title = 'Coca area',
        geo_scope='south america',
    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_mapa = fig

#--------------------------------------------------------------------------------------------------------
#incautaciones

inca_estupef = pd.read_csv("data/Incautaci_n_de_Estupefacientes.csv", parse_dates=["FECHA HECHO"])
inca_estupef['CANTIDAD'] = inca_estupef['CANTIDAD'].str.replace('.', '')
inca_estupef['CANTIDAD'] = inca_estupef['CANTIDAD'].astype(int)

# adding more variables to dataFrame : AÑO, MES, TONELADAS

inca_estupef['ANNO'] = pd.DatetimeIndex(inca_estupef['FECHA HECHO']).year
inca_estupef['MES'] = pd.DatetimeIndex(inca_estupef['FECHA HECHO']).month
inca_estupef['TONELADAS'] = (inca_estupef['CANTIDAD'] * 0.001)
df_inc = inca_estupef.groupby(['MES']).sum().reset_index()
# print(df_inc)
fig_inc = px.line(df_inc, x="MES", y="TONELADAS", title='Seizures of drugs')

#-------------------------------------------------------
#server y opciones


app.layout = html.Div([
    html.H4('Heat map of CocaArea'),
    dcc.Graph(figure=fig_mapa, style={'width': '90vh', 'height': '90vh','display': 'inline-block'}),
    dcc.Graph(figure = fig_inc,style={'display': 'inline-block'})
])
















app.run_server(debug=True)
