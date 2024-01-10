import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create dropdown options and year list
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'left', 'color': '#000000', 'font-size': 20}),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='Select Year'
    )),
    html.Div(id='output-container',className = "chart-grid", style={"display":"flex"})
])

# Callbacks
@app.callback(
    Output('output-container', 'children'),
    [Input('select-year', 'value'),
     Input('dropdown-statistics', 'value')]
)

def update_output_container(year, statistic_type):
    if statistic_type == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        if year:
            # Create graphs for recession period statistics
            if 'Recession' in data.columns and 'Automobile_Sales' in data.columns:
                yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
                chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                                  title="Average Automobile Sales fluctuation over Recession Period"))

                average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
                chart2 = dcc.Graph(figure=px.bar(average_sales, x="Vehicle_Type", y='Automobile_Sales',
                                                 title="Average Vehicles Sold by Vehicle Type during Recession"))

                exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
                chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                                 title='Total Advertising Expenditure by Vehicle Type'))

                chart4 = dcc.Graph(figure=px.bar(recession_data, x='Vehicle_Type', y='Automobile_Sales',
                                                 color='Unemployment_Rate',
                                                 labels={'Automobile_Sales': 'Automobile Sales',
                                                         'Unemployment_Rate': 'Unemployment Rate'},
                                                 title='Effect of Unemployment Rate on Vehicle Type and Sales'))

                return [
                    html.Div(className='chart-item', children=[html.Div(children=chart1),
                                                               html.Div(children=chart2)], style={'display': 'flex'}),
                    html.Div(className='chart-item', children=[html.Div(children=chart3),
                                                               html.Div(children=chart4)], style={'display': 'flex'})
                ]
            
            else:
                return html.Div("Required columns not found in data.")
        else:
            return html.Div("Select a year for Recession Period Statistics.")

    elif statistic_type == 'Yearly Statistics':
        yearly_data = data[data['Year'] == year]

        if 'Year' in data.columns and 'Automobile_Sales' in data.columns:
            yas = data.groupby('Year')['Automobile_Sales'].sum().reset_index()
            chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                              title="Yearly Automobile Sales"))

            monthly_sales = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
            chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales',
                                              title="Total Monthly Automobile Sales"))

            average_sales_by_type = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            chart3 = dcc.Graph(figure=px.bar(average_sales_by_type, x='Vehicle_Type', y='Automobile_Sales',
                                             title='Average Vehicles Sold by Vehicle Type in {}'.format(year)))

            total_expenditure_by_type = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            chart4 = dcc.Graph(figure=px.pie(total_expenditure_by_type, values='Advertising_Expenditure',
                                             names='Vehicle_Type',
                                             title='Total Advertising Expenditure by Vehicle Type in {}'.format(year)))

            return [
                html.Div(className='chart-item', children=[html.Div(children=chart1), html.Div(children=chart2)],
                         style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=chart3), html.Div(children=chart4)],
                         style={'display': 'flex'})
            ]
        else:
            return html.Div("Required columns not found in data.")
    else:
        return html.Div("Invalid selection.")


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
