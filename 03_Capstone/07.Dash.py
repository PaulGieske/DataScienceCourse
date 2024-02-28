# Install if necessary:
#   python3 -m pip install packaging
#   python3 -m pip install pandas dash
#   pip3 install httpx==0.20 dash plotly
#   sudo pip3 install setuptools

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(spacex_df.columns)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                      value='ALL',
                                                      options=[{'label':'All Sites','value':'ALL'},
                                                               {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                               {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                                               {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                               {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}])),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',min=0,max=10000,
                                                         step=1000,marks={0: '0',
                                                                          2500: '2500',
                                                                          5000: '5000',
                                                                          7500: '7500',
                                                                          10000:'10000'},
                                                         value=[0, 10000])),
                                                         

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if (entered_site == "ALL"):
        fig = px.pie(spacex_df, values='class',names='Launch Site')
        return fig
    else:
        plot_data=spacex_df[spacex_df["Launch Site"]==entered_site]
        print(entered_site)
        fig = px.pie(plot_data, names='class')
        return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='payload-slider', component_property='value'),
               Input(component_id='site-dropdown', component_property='value')])

def get_scatter(payload_range,site):
    #print(payload_range)
    #print(site)
    data = spacex_df[spacex_df["Payload Mass (kg)"]>payload_range[0]]
    data = data[data["Payload Mass (kg)"]<payload_range[1]]
    #print(data.head())
    #print(data["Payload Mass (kg)"].min())
    #print(data["Payload Mass (kg)"].max())

    if (site!='ALL'):
        data = data[data["Launch Site"] == site]

    fig = px.scatter(data,x='Payload Mass (kg)',y='class',color='Booster Version Category')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
