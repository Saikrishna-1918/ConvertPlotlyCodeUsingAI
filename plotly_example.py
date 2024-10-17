import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import webbrowser

# Updated JSON data for states, including Arizona and Arkansas
json_data = '''
[
  {
    "State": "Alabama",
    "Total": 5028090,
    "WhiteTotal": 3329010,
    "BlackTotal": 1326343,
    "IndianTotal": 21122,
    "AsianTotal": 69808,
    "HawaiianTotal": 2253,
    "OtherTotal": 279556,
    "TwoOrMoreTotal": 185632
  },
  {
    "State": "Alaska",
    "Total": 734821,
    "WhiteTotal": 450472,
    "BlackTotal": 23395,
    "IndianTotal": 104957,
    "AsianTotal": 47464,
    "HawaiianTotal": 11209,
    "OtherTotal": 97324,
    "TwoOrMoreTotal": 82727
  },
  {
    "State": "Arizona",
    "Total": 7172280,
    "WhiteTotal": 4781701,
    "BlackTotal": 327077,
    "IndianTotal": 297590,
    "AsianTotal": 240642,
    "HawaiianTotal": 14116,
    "OtherTotal": 1511155,
    "TwoOrMoreTotal": 961794
  },
  {
    "State": "Arkansas",
    "Total": 3018670,
    "WhiteTotal": 2193344,
    "BlackTotal": 456693,
    "IndianTotal": 16840,
    "AsianTotal": 47413,
    "HawaiianTotal": 11117,
    "OtherTotal": 293258,
    "TwoOrMoreTotal": 203476
  }
]
'''

# Parse the JSON data
# Parse the JSON data
data_dict = json.loads(json_data)

# Prepare the data for the bar chart
bar_data = []
for state_data in data_dict:
    state = state_data['State']
    bar_data.append({
        'State': state,
        'White': state_data['WhiteTotal'],
        'Black': state_data['BlackTotal'],
        'Indian': state_data['IndianTotal'],
        'Asian': state_data['AsianTotal'],
        'Hawaiian': state_data['HawaiianTotal'],
        'Other': state_data['OtherTotal'],
        'TwoOrMore': state_data['TwoOrMoreTotal']
    })

# Convert to DataFrame for bar chart
df_bar = pd.DataFrame(bar_data)

# Initialize the Dash app
app = Dash(__name__)

# App layout with CSS for styling
app.layout = html.Div(style={'font-family': 'Arial', 'background-color': '#f9f9f9', 'padding': '20px'}, children=[
    html.H1("Population Distribution in Selected States", style={'textAlign': 'center', 'color': '#333'}),
    
    # Bar chart
    dcc.Graph(
        id='state-bar-chart',
        figure=px.bar(
            df_bar, 
            x='State', 
            y=df_bar.columns[1:], 
            title='Population by Race and Ethnicity',
            labels={'value': 'Population Count', 'variable': 'Race/Ethnicity'},
            template='plotly_white',  # Light background for charts
            color_discrete_sequence=px.colors.qualitative.Bold  # Custom color scheme
        ).update_layout(
            title_font_size=22,
            title_x=0.5,
            xaxis_tickangle=-45,
            xaxis_title=None,
            yaxis_title='Population Count',
            hovermode="x unified",
            margin=dict(l=40, r=40, t=40, b=40),
            legend_title_text='Race/Ethnicity',
            legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.01),
        )
    ),

    # Pie chart
    dcc.Graph(
        id='state-pie-chart',
        # Initially empty pie chart
        figure=px.pie(title='Click a state in the bar chart to see the population breakdown.').update_layout(
            title_font_size=18,
            title_x=0.5,
            margin=dict(l=40, r=40, t=40, b=40)
        )
    )
])

# Callback to update the pie chart based on bar chart clicks
@app.callback(
    Output('state-pie-chart', 'figure'),
    Input('state-bar-chart', 'clickData')
)
def update_pie_chart(clickData):
    if clickData is None:
        # Return an empty pie chart if no state is selected
        return px.pie(title='Click a state in the bar chart to see the population breakdown.')
    
    # Get the selected state from the click data
    selected_state = clickData['points'][0]['x']
    selected_data = df_bar[df_bar['State'] == selected_state]

    # Ensure the column names are strings and values are float
    names = selected_data.columns[1:].astype(str)
    values = selected_data.iloc[0, 1:].astype(float)

    # Return the pie chart figure
    return px.pie(
        names=names,
        values=values,
        title=f'{selected_state} Population Breakdown',
        color_discrete_sequence=px.colors.sequential.Blues,  # Color gradient for pie chart
        hole=0.4  # Donut style pie chart for better readability
    ).update_traces(
        textposition='inside', 
        textinfo='percent+label',  # Show percentage and labels
        hoverinfo='label+percent+value'
    ).update_layout(
        title_font_size=20,
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True
    )

# Run the app
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050')  # Automatically open in the default browser
    app.run_server(debug=True, port=8050)