import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data/historical_automobile_sales.csv"
df = pd.read_csv(url)

app = dash.Dash(__name__)
server = app.server

year_list = [i for i in range(1980, 2024)]

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value='Select Statistics',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-direction': 'column'})
    ])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]
        
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                           title="Average Automobile Sales Fluctuation during Recession Period")
        
        av_veh = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = px.bar(av_veh, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type during Recession")
        
        exp_veh = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = px.pie(exp_veh, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Advertising Expenditure Share by Vehicle Type during Recession")
        
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = px.line(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                           title="Effect of Unemployment Rate on Vehicle Type and Sales during Recession")
        
        return [
            html.Div(className='chart-item', children=[dcc.Graph(figure=R_chart1), dcc.Graph(figure=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=R_chart3), dcc.Graph(figure=R_chart4)], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]
        
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Average Automobile Sales Trend")
        
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = px.line(mas, x='Month', y='Automobile_Sales', title="Total Monthly Automobile Sales for " + str(input_year))
        
        veh_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_call = "Average Vehicles Sold by Vehicle Type in " + str(input_year)
        Y_chart3 = px.bar(veh_sales, x='Vehicle_Type', y='Automobile_Sales', title=Y_call)
        
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Advertisement Expenditure by Vehicle Type in " + str(input_year))
        
        return [
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart1), dcc.Graph(figure=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart3), dcc.Graph(figure=Y_chart4)], style={'display': 'flex'})
        ]
    
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
