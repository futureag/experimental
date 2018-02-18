import pygal
import requests
import json

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getAtlasPHChart():
    r = requests.get('http://127.0.0.1:5984/mvp_sensor_data/_design/doc/_view/attribute_value?startkey=["ph",{}]&endkey=["ph"]&descending=true&limit=60')
    print r

    v_lst = [float(x['value']['value']) for x in r.json()['rows']]
    ts_lst = [x['value']['timestamp'] for x in r.json()['rows']]


    line_chart = pygal.Line()
    line_chart.title = 'ph'
    line_chart.y_title="h+"
    line_chart.x_title="Timestamp (hover over to display date)"
    #need to reverse order to go from earliest to latest
    ts_lst.reverse()
    line_chart.x_labels = ts_lst
    #need to reverse order to go from earliest to latest
    v_lst.reverse()
    line_chart.add('PH', v_lst)
    line_chart.render_to_file('/home/pi/MVP/web/ph_chart.svg')

getAtlasPHChart()
