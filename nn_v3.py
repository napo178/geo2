import pandas as pd
import geopandas as gpd
import folium
from shapely.ops import nearest_points
from shapely.geometry import LineString, Point, MultiPoint
import streamlit as st
from streamlit_folium import folium_static



#kiosk = pd.read_csv("kiosk.csv", delimiter = ";")
#customers = pd.read_csv("customers.csv", delimiter = ";")
kioskuu = ""
customersuu = ""


st.write("Nearest Neighbour example")   
kioskuu = st.file_uploader("Choose a kiosk file")
customersuu = st.file_uploader("Choose a customer file")
if customersuu and kioskuu is not None:
  kiosku = pd.read_csv(kioskuu, delimiter = ";")
  customersu = pd.read_csv(customersuu, delimiter = ";")
     


   

  def create_gdf(df, x= "x", y="y"):
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[y], df[x]), crs=("EPSG:3857"))

  

  kiosk = create_gdf(kiosku)
  customers = create_gdf(customersu)



  def calculate_nearest(row, destination, val, col="geometry"):

    # 1 - create unary union    
    dest_unary = destination["geometry"].unary_union


    # 2 - find closest point
    nearest_geom = nearest_points(row[col], dest_unary)


    # 3 - Find the corresponding geom
    match_geom = destination.loc[destination.geometry == nearest_geom[1]]


    # 4 - get the corresponding value
    match_value = match_geom[val].to_numpy()[0]


    return match_value


  customers["nearest_geom"] = customers.apply(calculate_nearest, destination=kiosk, val="geometry", axis=1)


  customers.head()


  kiosk.crs = crs=("epsg:4326")
  customers.crs = crs=("epsg:4326")

  customer = []

  coord_list = [(x,y) for x,y in zip(customers['geometry'].x , customers['geometry'].y)]
  nearest_list = [(x,y) for x,y in zip(customers['nearest_geom'].x , customers['nearest_geom'].y)]

  cocenter = coord_list[1]

  m = folium.Map(cocenter, tiles="CartoDb dark_matter", zoom_start = 11,  crs='EPSG3857')






  for lin in range(len(nearest_list)):
    folium.PolyLine([coord_list[lin],nearest_list[lin]]).add_to(m)
    
  kiosk_points = zip(kiosk.x,kiosk.y)
  for location in kiosk_points:
    folium.CircleMarker(location=location, color="red",   radius=6).add_to(m)
    
  for location_ in coord_list:
    folium.CircleMarker(location=location_, color="blue",   radius=1).add_to(m)

  folium_static(m)



else:
  st.write("Please upload a file")
   


