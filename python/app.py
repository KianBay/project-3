from flask import Flask, render_template
import json
import plotly
import plotly.express as px
from db import db
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

myDb = db('root', 'newpass', 'project3', 'measurements')

app = Flask(__name__)
@app.route('/')
def index():
    rooms = myDb.get_unique_classrooms('location', 'Classroom')
    return render_template('index.html', len=len(rooms), rooms=rooms)

@app.route('/graph/<classroom>')
def graph(classroom):
    mac = myDb.get_match_on_room('location', classroom)
    df = myDb.db_mac_to_df('measurements', mac)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df['ts'], y=df['temperature'], name='Temperature', line=dict(color='Crimson')), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['ts'], y=df['humidity'], name='Humidity', line=dict(color='CornflowerBlue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['ts'], y=df['lightIntensity'], name='Light Intensity', line=dict(color='Burlywood')), secondary_y=True)

    fig.update_layout(title_text="The Holy Trifecta of Data") #Can add a ton of parameters here; height, width etc

    header ='Sensor data for classroom ' + classroom
    description = 'The data is collected in a 5-minute interval in a static position in the given classroom.'
    #print(classroom)
    #graphJSON = fig.to_json()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graphing.html', graphJSON=graphJSON, header=header,description=description)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4848, debug=True)



