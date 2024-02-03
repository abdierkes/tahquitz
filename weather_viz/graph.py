import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
from dotenv import load_dotenv
import psycopg2
import plotly.express as px
from datetime import date
import flask

load_dotenv()

#data aquisition
db_params = {"user": "postgres",
             "password": os.getenv("PASSWORD"),
             "host": os.getenv("HOST"),
             "port": os.getenv("PORT"),
             "dbname": os.getenv("DBNAME")
             }

#obtain data
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

select_query = '''SELECT * FROM tahquitz_weather
                  ORDER BY date, hour
                '''

cur.execute(select_query)

data = cur.fetchall()
col = [col[0] for col in cur.description]

df_tah = pd.DataFrame(data, columns=col)

conn.close()

#app
server = flask.Flask(__name__)
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Tahquitz Weather Analyzer"),
        html.P(
            children=(
                "Visualize weather patterns for Tahquitz Rock."
            ),
        ),
        dcc.DatePickerRange(
            id='date_picker_range',
            display_format='YYYY-MM-DD',
            start_date=df_tah['date'].min(),
            end_date=df_tah['date'].max(),
            end_date_placeholder_text="Select a date",
        ),
        html.Div(id='output-container-date-picker-range'),
        dcc.Graph(id='temperature_graph')
    ]
)

@app.callback(
    Output('temperature_graph', 'figure'),
    [Input('date_picker_range', 'start_date'),
     Input('date_picker_range', 'end_date')]
)
def update_graph(start_date, end_date):
    df_tah_filtered = df_tah[(df_tah['date'] >= start_date) & (df_tah['date'] <= end_date)]
    fig_tah = px.scatter(df_tah_filtered, x="hour", y="temperature", color="date")

    return fig_tah

if __name__ == "__main__":
    app.run_server(debug=True)