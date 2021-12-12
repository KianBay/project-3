from flask import Flask, render_template
import json
import plotly
import plotly.express as px
from db import db
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
myDb = db('root', 'newpass', 'project3', 'measurements')

df = myDb.db_to_df()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=df['ts'], y=df['temperature'], name='Temperature'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['ts'], y=df['humidity'], name='Humidity'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['ts'], y=df['lightIntensity'], name='Light Intensity'), secondary_y=True)


fig.update_layout(title_text="Lets do this") #Can add a ton of parameters here; height, width etc

fig.show()
