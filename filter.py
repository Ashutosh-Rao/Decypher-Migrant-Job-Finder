from geopy.geocoders import Nominatim
import geopy.distance
import pandas as pd
import numpy as np
import geocoder
def get_latlng(city):
    co_ords = None
    while(co_ords is None):
        g = geocoder.arcgis('{}'.format(city))
        co_ords = g.latlng
    return co_ords

def get_distance(emp_loc,city):
    coords_1 = emp_loc
    coords_2 = city
    return geopy.distance.vincenty(coords_1, coords_2).km

def to_html():
    a = pd.read_csv("final.csv")
    a.to_html("display.html")
    html_file = a.to_html()

def filter(emp_city):
    df = pd.read_csv("workers.csv")
    coords_cities = [ get_latlng(city) for city in df["city"].tolist() ]
    df_coords = pd.DataFrame(coords_cities, columns=['Lat1', 'Long1'])
    #df['Latitude'] = df_coords['Lat1']
    #df['Longitude'] = df_coords['Long1']
    #get employer loc
    emp_loc = get_latlng(emp_city)
    dist_list = [get_distance(emp_loc,i) for i in coords_cities]
    dist_df = pd.DataFrame(dist_list,columns=["distance"])
    df["distance"] = dist_df["distance"]
    df.sort_values(by=['distance'], inplace=True)
    df.to_csv("final.csv",index=False)
    to_html()
    return
#filter("delhi")
