from flask import Flask, render_template, request
from flask import jsonify
import pandas as pd
import json,shutil,os
import numpy as np
app = Flask(__name__)
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

def filter(emp_city,skill,min_age,max_age,gender):
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
    df = df[df['skills'] == skill]
    df = df[df['age'] >= min_age]
    df = df[df['age'] <= max_age]
    df = df[df['gender'] == gender]
    #os.remove("C:\\Users\\Admin\\Desktop\\hackathon\\try\\templates\\display.html")
    #os.remove("C:\\Users\\Admin\\Desktop\\hackathon\\try\\final.csv")
    df.to_csv("final.csv",index=False)
    to_html()
    os.chdir("C:\\")
    shutil.move("C:\\Users\\Admin\\Desktop\\final\\display.html","C:\\Users\\Admin\\Desktop\\final\\templates")
    return

@app.route('/')
def student():
   return render_template('filter.html')

"""@app.route('/getdata',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      json_data = list(request.form.to_dict().values())
      df = pd.DataFrame([json_data],columns=['fullname','contact_no','skills','city','age','gender','emp_contact'])
      df.to_csv("workers.csv",mode='a', header=False)
      return render_template("filter.html")"""

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      json_data = list(request.form.to_dict().values())
      #df = pd.DataFrame([json_data],columns=['City','skills','sage','mage','age'])
      #df.to_csv("filter.csv",mode='a', header=False)
      filter(json_data[0],json_data[1],int(json_data[2]),int(json_data[3]),json_data[4])
      return render_template("display.html")

if __name__ == '__main__':
   app.run(debug = True)
