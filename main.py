import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import json
import numpy as np

# TODO: all color hex codes
colors = {
    'basic background': '#0D1012',
    'card background': '#202428',
    'text': '#7FDBFF',
    'confirmed card1 text': '#FF5858',
    'recovered card1 text': '#34DB3E',
    'death card1 text': '#FFF04E',
    'white': '#FFFFFF',
    'label border': '#636EFC',
    'death line': '#FB902F',
    'death text': '#FFEFA6'
}

# TODO: text style
header1_font = {
    'font-family': 'monospace',
    'font-size': '40px',
    'font-weight': '900'
}

header2_font = {
    'font-family': 'monospace',
    'font-size': '25px',
    'font-weight': '900'
}

card1_font1 = {
    'font-family': 'monospace',
    'font-size': '23px',
    'font-weight': '900'
}

card1_font2 = {
    'font-family': 'monospace',
    'font-size': '52px',
    'font-weight': '900'
}

card1_header_font = {
    'font-family': 'monospace',
    'font-size': '30px',
    'font-weight': '900'
}

label_font = {
    'font-family': 'monospace',
    'font-size': '20px',
    'font-weight': '900'
}

# TODO: map
uk_states = json.load(open("dataset/uk_regions.geojson", 'r'))

state_id_map = {}
for feature in uk_states['features']:
    feature['id'] = feature['properties']['rgn19cd']
    state_id_map[feature['properties']['rgn19nm']] = feature['id']

df = pd.read_csv("dataset/Cases_by_date_reported_only.csv")
df['Density'] = df['cumCasesByPublishDate']
df['id'] = df['areaName'].apply(lambda x: state_id_map[x])

df['CasesScale'] = np.log10(df['Density'])

map_fig = px.choropleth_mapbox(df,
                               locations='id',
                               geojson=uk_states,
                               color='CasesScale',
                               hover_name='areaName',
                               hover_data=['cumCasesByPublishDate'],
                               mapbox_style="carto-positron",
                               zoom=4,
                               opacity=0.5,
                               center={'lat': 54.5, 'lon': -5})

map_fig.update_layout(
    paper_bgcolor=colors['card background'],
    font_color=colors['text']
)

# TODO: three card: confirmed, recovered, death
# confirmed cases
# read cumCases data
cumCases = pd.read_csv('dataset/Cases_by_date_reported.csv', parse_dates=['date'])
# separate data
latest_eng_cumCases = cumCases.query('areaName == "England"')
latest_ire_cumCases = cumCases.query('areaName == "Northern Ireland"')
latest_scot_cumCases = cumCases.query('areaName == "Scotland"')
latest_wales_cumCases = cumCases.query('areaName == "Wales"')
# get latest data
a = latest_eng_cumCases.loc[latest_eng_cumCases.index[0], 'cumCasesByPublishDate']
b = latest_ire_cumCases.loc[latest_ire_cumCases.index[0], 'cumCasesByPublishDate']
c = latest_scot_cumCases.loc[latest_scot_cumCases.index[0], 'cumCasesByPublishDate']
d = latest_wales_cumCases.loc[latest_wales_cumCases.index[0], 'cumCasesByPublishDate']
# compute latest cumCases
latest_cumCases = a + b + c + d

# death cases
# read cumDaily_deaths data
cumDaily_deaths = pd.read_csv('dataset/cumDaily_deaths.csv', parse_dates=['date'])
# compute latest total death cases
total_deaths = cumDaily_deaths.groupby('date').sum().reset_index()
latest_total_deaths = total_deaths.loc[total_deaths.index[-1], 'cumDailyNsoDeathsByDeathDate']

# TODO: daily confirmed cases diagram by region
# separate data
eng_daily_cases = cumCases.query('areaName == "England"')
ire_daily_cases = cumCases.query('areaName == "Northern Ireland"')
scot_daily_cases = cumCases.query('areaName == "Scotland"')
wales_daily_cases = cumCases.query('areaName == "Wales"')

eng_daily_cases_fig = px.line(eng_daily_cases,
                              x="date", y="newCasesByPublishDate",
                              title='Daily Confirmed Cases in England')
eng_daily_cases_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['text']
)

ire_daily_cases_fig = px.line(ire_daily_cases,
                              x="date", y="newCasesByPublishDate",
                              title='Daily Confirmed Cases in Northern Ireland')
ire_daily_cases_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['text']
)

scot_daily_cases_fig = px.line(scot_daily_cases,
                               x="date", y="newCasesByPublishDate",
                               title='Daily Confirmed Cases in Scotland')
scot_daily_cases_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['text']
)

wales_daily_cases_fig = px.line(wales_daily_cases,
                                x="date", y="newCasesByPublishDate",
                                title='Daily Confirmed Cases in Wales')
wales_daily_cases_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['text']
)


# TODO: daily death cases diagram by region
# read daily death cases data
daily_deaths = pd.read_csv('dataset/Daily_deaths.csv', parse_dates=['date'])
# separate data
eng_daily_deaths = daily_deaths.query('areaName == "England"')
ire_daily_deaths = daily_deaths.query('areaName == "Northern Ireland"')
scot_daily_deaths = daily_deaths.query('areaName == "Scotland"')
wales_daily_deaths = daily_deaths.query('areaName == "Wales"')

eng_daily_deaths_fig = px.line(eng_daily_deaths,
                               x="date", y="newDailyNsoDeathsByDeathDate",
                               title='Daily Deaths in England')
eng_daily_deaths_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['death text']
)
eng_daily_deaths_fig.update_traces(line_color=colors['death line'])

ire_daily_deaths_fig = px.line(ire_daily_deaths,
                               x="date", y="newDailyNsoDeathsByDeathDate",
                               title='Daily Deaths in Northern Ireland')
ire_daily_deaths_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['death text']
)
ire_daily_deaths_fig.update_traces(line_color=colors['death line'])

scot_daily_deaths_fig = px.line(scot_daily_deaths,
                                x="date", y="newDailyNsoDeathsByDeathDate",
                                title='Daily Deaths in Scotland')
scot_daily_deaths_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['death text']
)
scot_daily_deaths_fig.update_traces(line_color=colors['death line'])

wales_daily_deaths_fig = px.line(wales_daily_deaths,
                                 x="date", y="newDailyNsoDeathsByDeathDate",
                                 title='Daily Deaths in Wales')
wales_daily_deaths_fig.update_layout(
    plot_bgcolor=colors['card background'],
    paper_bgcolor=colors['card background'],
    font_color=colors['death text']
)
wales_daily_deaths_fig.update_traces(line_color=colors['death line'])

# daily death diagram stylesheet
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# TODO: create app
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)


# TODO: whole layout
app.layout = html.Div(children=[
    html.H1(
        children='COVID-19 Tracker',
        style={
            'color': colors['text'],
            # 'font-family': 'monospace',
            'font-size': header1_font['font-size'],
            'background': colors['basic background'],
            'padding-top': '40px',
            'padding-left': '80px'
        }
    ),

    html.Div(
        children='United Kingdom',
        style={
            'color': colors['text'],
            'font-size': header2_font['font-size'],
            'background': colors['basic background'],
            'margin-bottom': '30px',
            'padding-left': '80px',
            'display': 'inline-block'
        }
    ),

    html.Table(
        html.Tr([
            html.Td([
                html.Div("Latest Confirmed Cases (By Region)", style={
                    'font-size': card1_header_font['font-size'],
                    'color': colors['text'],
                    'textAlign': 'center',
                    'padding-top': '10px'
                }),
                dcc.Graph(
                    id='map',
                    figure=map_fig,
                    style={
                        'width': '855px',
                        'height': '555px',
                    }
                )
            ], style={
                'background': colors['card background'],
                'display': 'inline-block',
                'margin-left': '70px',
                'margin-right': '25px',
                'border': '10px solid #202428',
                'border-radius': '30px'
            }),
            html.Td([
                html.Div(
                    children=[
                        html.Div(
                            children='Confirmed cases',
                            style={
                                'color': colors['white'],
                                'background': colors['card background'],
                                'font-size': card1_font1['font-size']
                            }
                        ),
                        html.Div(
                            children=latest_cumCases,
                            style={
                                'font-size': card1_font2['font-size'],
                                'color': colors['confirmed card1 text'],
                                'margin-top': '20px',
                                'textAlign': 'center'
                            }
                        )
                    ],
                    style={
                        'width': '240px',
                        'height': '120px',
                        'margin-left': '30px',
                        'margin-bottom': '40px',
                        'padding': '30px',
                        'border-radius': '20px',
                        'background': colors['card background'],
                    }
                ),
                html.Div(
                    children=[
                        html.Div(
                            children='Recovered cases',
                            style={
                                'color': colors['white'],
                                'background': colors['card background'],
                                'font-size': card1_font1['font-size']
                            }
                        ),
                        html.Div(
                            children='9259179',
                            style={
                                'font-size': card1_font2['font-size'],
                                'color': colors['recovered card1 text'],
                                'margin-top': '20px',
                                'textAlign': 'center'
                            }
                        )
                    ],
                    style={
                        'width': '240px',
                        'height': '120px',
                        'margin-left': '30px',
                        'margin-top': '30px',
                        'margin-bottom': '30px',
                        'padding': '30px',
                        'border-radius': '20px',
                        'background': colors['card background'],
                    }
                ),
                html.Div(
                    children=[
                        html.Div(
                            children='Death cases',
                            style={
                                'color': colors['white'],
                                'background': colors['card background'],
                                'font-size': card1_font1['font-size']
                            }
                        ),
                        html.Div(
                            children=latest_total_deaths,
                            style={
                                'font-size': card1_font2['font-size'],
                                'color': colors['death card1 text'],
                                'margin-top': '20px',
                                'textAlign': 'center'
                            }
                        )
                    ],
                    style={
                        'width': '240px',
                        'height': '120px',
                        'margin-left': '30px',
                        'margin-top': '40px',
                        'padding': '30px',
                        'border-radius': '20px',
                        'background': colors['card background'],
                    }
                )
            ])
        ])
    ),

    html.Div(
        dcc.Tabs([
            dcc.Tab(label='England', children=[
                dcc.Graph(
                    figure=eng_daily_cases_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '20px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #636EFC',
                'color': colors['text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Northern Ireland', children=[
                dcc.Graph(
                    figure=ire_daily_cases_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #636EFC',
                'color': colors['text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Scotland', children=[
                dcc.Graph(
                    figure=scot_daily_cases_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #636EFC',
                'color': colors['text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Wales', children=[
                dcc.Graph(
                    figure=wales_daily_cases_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #636EFC',
                'color': colors['text'],
                'font-size': label_font['font-size']
            }),
        ]),
        style={
            'width': '84%',
            'background': colors['card background'],
            'border-radius': '20px',
            'margin-left': '70px',
            'margin-right': '70px',
            'margin-top': '40px',
            'padding-top': '40px',
            'padding-left': '30px',
            'padding-right': '30px'
        }
    ),

    html.Div(
        dcc.Tabs([
            dcc.Tab(label='England', children=[
                dcc.Graph(
                    figure=eng_daily_deaths_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '20px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #FB902F',
                'color': colors['death text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Northern Ireland', children=[
                dcc.Graph(
                    figure=ire_daily_deaths_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #FB902F',
                'color': colors['death text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Scotland', children=[
                dcc.Graph(
                    figure=scot_daily_deaths_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #FB902F',
                'color': colors['death text'],
                'font-size': label_font['font-size']
            }),
            dcc.Tab(label='Wales', children=[
                dcc.Graph(
                    figure=wales_daily_deaths_fig,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'margin-left': '10px',
                        'margin-top': '10px'
                    }
                )
            ], style={
                'background-color': colors['card background'],
                'border': '1px solid #FB902F',
                'color': colors['death text'],
                'font-size': label_font['font-size']
            }),
        ]),
        style={
            'width': '84%',
            'background': colors['card background'],
            'border-radius': '20px',
            'margin-left': '70px',
            'margin-right': '70px',
            'margin-top': '40px',
            'padding-top': '40px',
            'padding-left': '30px',
            'padding-right': '30px'
        }
    ),
], style={
    'background': colors['basic background'],
    'padding-bottom': '40px'
})

if __name__ == '__main__':
    app.run_server(debug=True)
