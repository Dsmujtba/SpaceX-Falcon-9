# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from spacex_api import fetch_spacex_data

# Load the data
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Custom index_string
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>SpaceX Launch Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {background-color: #1e1e1e; color: #ffffff;}
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', 'css/styles.css'], index_string=index_string)

# Define the app layout
app.layout = html.Div(className='container', children=[
    html.Div([
        html.Img(src='https://cognitiveclass.ai/wp-content/uploads/2018/10/cc-logo-square.png',
                 style={'width': '10%', 'float': 'right', 'display': 'inline-block'}),
        html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#ffffff'}),
        html.Div([
            html.Div([
                html.H6('Total Launches', style={'color': '#ffffff'}),
                html.P(id='total-launches', className='card'),
            ], className='three columns'),
            html.Div([
                html.H6('Total Success', style={'color': '#ffffff'}),
                html.P(id='total-success', className='card'),
            ], className='three columns'),
            html.Div([
                html.H6('Total Failures', style={'color': '#ffffff'}),
                html.P(id='total-failures', className='card'),
            ], className='three columns'),
        ], className='row'),

        html.Div([
            dcc.Dropdown(id='site-dropdown',
                         options=[
                             {'label': 'All Sites', 'value': 'ALL'},
                             {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                             {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                             {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                             {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                         ],
                         value='ALL',
                         placeholder="Select a Launch Site here",
                         searchable=True,
                         style={'width': '60%', 'margin': 'auto'}
                         ),
        ], style={'textAlign': 'center'}),

        dcc.Graph(id='success-pie-chart', style={'width': '100%', 'height': '600px', 'margin': 'auto'}),
        html.Br(),
        html.P("Payload range (Kg):", style={'textAlign': 'center', 'fontSize': 18}),
        dcc.RangeSlider(id='payload-slider',
                        min=0, max=10000, step=1000,
                        marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000',
                               4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000',
                               8000: '8000', 9000: '9000', 10000: '10000'},
                        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
                        ),
        dcc.Graph(id='success-payload-scatter-chart', style={'width': '100%', 'height': '600px', 'margin': 'auto'}),
        html.Br(),
        dcc.Graph(id='booster-version-chart', style={'width': '100%', 'height': '600px', 'margin': 'auto'}),
        html.Div(id='globe-container', className='container'),
        html.Canvas(id='mini-game', className='container')
    ], style={'width': '80%', 'margin': 'auto', 'paddingTop': '50px'})
])

# Callbacks
@app.callback(
    [Output('total-launches', 'children'),
     Output('total-success', 'children'),
     Output('total-failures', 'children'),
     Output('payload-slider', 'value')],
    [Input('site-dropdown', 'value')]
)
def update_summary_cards(entered_site):
    filtered_df = spacex_df
    total_launches = filtered_df.shape[0]
    total_success = filtered_df[filtered_df['class'] == 1].shape[0]
    total_failures = filtered_df[filtered_df['class'] == 0].shape[0]
    payload_min = filtered_df['Payload Mass (kg)'].min()
    payload_max = filtered_df['Payload Mass (kg)'].max()

    return total_launches, total_success, total_failures, [payload_min, payload_max]

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site',
                     color_discrete_map={'1': '#00cc96', '0': '#EF553B'})
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success Launches for site {entered_site}',
                     color_discrete_map={'1': '#00cc96', '0': '#EF553B'})
    fig.update_layout(paper_bgcolor='#1e1e1e', font_color='#ffffff')
    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        mask = (filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])
        filtered_df = filtered_df[mask]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload Success Rate for All Sites',
                         color_discrete_map={'1': '#00cc96', '0': '#EF553B'})
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        mask = (filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])
        filtered_df = filtered_df[mask]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload Success Rate for site {entered_site}',
                         color_discrete_map={'1': '#00cc96', '0': '#EF553B'})
    fig.update_layout(paper_bgcolor='#1e1e1e', font_color='#ffffff')
    return fig

@app.callback(Output(component_id='booster-version-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_booster_chart(entered_site):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    fig = px.bar(filtered_df, x='Booster Version Category', y='class',
                 color='Booster Version Category', barmode='group',
                 title=f'Success Count by Booster Version for {entered_site if entered_site != "ALL" else "All Sites"}',
                 color_discrete_map={'1': '#00cc96', '0': '#EF553B'})
    fig.update_layout(paper_bgcolor='#1e1e1e', font_color='#ffffff')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)