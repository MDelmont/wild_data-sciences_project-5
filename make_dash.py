from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import make_fig
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
serie = make_fig.get_list_date()
fig1 = make_fig.get_fig_line_plot('by_day','country',serie[19],'brut')
fig2 = make_fig.get_fig_line_plot('sum','country',serie[19],'brut')
fig3 = make_fig.get_fig_map_monde('by_day','country',serie[19],'brut')
fig4 = make_fig.get_fig_map_monde('sum','country',serie[19],'brut')

list_cont_count = make_fig.get_list_cont_count()
numdate= [x for x in range(len(serie.unique()))]
app.layout = html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                                id='zone_geo',
                                options=[{'label': i, 'value': i} for i in ['continent',  'country']],
                                value='country'
                                ),
                    ],style={'width': '49%', 'display': 'inline-block'}), 

                html.Div([
                            dcc.Dropdown(
                                 id='reference_echelle',
                                options=[{'label': i, 'value': i} for i in ['population', 'density','brut']],
                                value='brut'
                        
                            ),
                ],style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                                        id='Select_pays_or_continent',
                                        options=[{'label': i, 'value': i} for i in list_cont_count],
                                        multi=True,
                                        value = list_cont_count
                                    ),
                ]),
                
                html.Div([

                    dcc.Slider(
                            id='Date_select',
                            min=numdate[0], #the first date
                            max=numdate[-1], #the last date
                            value=numdate[-1], #default: last date
                            marks = {numd:date.strftime('%d/%m/%Y') for numd,date in zip(numdate, serie.dt.date.unique())})
                ]),     


                
                ]),
                html.Div([
                    html.Div([

                          dcc.Graph(
                                        id='by_day_graph_line',
                                        figure=fig1,
                                        style={'width': '100%'}
                                    ),


                    ]),
                    html.Div([

                            dcc.Graph(
                                        id='by_sum_graph_line',
                                        figure=fig2,
                                        style={'width': '100%'}
                                    ),
                      
                    ])
                ],style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    html.Div([

                          dcc.Graph(
                                        id='by_day_graph_map',
                                        figure=fig3,
                                        style={'width': '100%'}
                                    ),


                    ]),
                    html.Div([

                            dcc.Graph(
                                        id='by_sum_graph_map',
                                        figure=fig4,
                                        style={'width': '100%'}
                                    ),
                      
                    ])
                ],style={'width': '49%', 'display': 'inline-block'})
        

            ])



@app.callback(
    Output('by_day_graph_line', 'figure'),
    Output('by_sum_graph_line', 'figure'),
    Output('by_day_graph_map', 'figure'),
    Output('by_sum_graph_map', 'figure'),
    Input('zone_geo', 'value'),
    Input('reference_echelle', 'value'),
    Input('Date_select', 'value'),
    Input('Select_pays_or_continent', 'value'))
def update_gaphes(zone_geo,reference_echelle,Date_select,Select_pays_or_continent):
    serie = make_fig.get_list_date()

    fig1=make_fig.get_fig_line_plot('by_day',zone_geo,serie[Date_select+1],reference_echelle,Select_pays_or_continent)
    fig2=make_fig.get_fig_line_plot('sum',zone_geo,serie[Date_select+1],reference_echelle,Select_pays_or_continent)
    fig3 = make_fig.get_fig_map_monde('by_day',zone_geo,serie[Date_select+1],reference_echelle,Select_pays_or_continent)
    fig4 = make_fig.get_fig_map_monde('sum',zone_geo,serie[Date_select+1],reference_echelle,Select_pays_or_continent)
    return fig1,fig2,fig3,fig4



@app.callback(
    Output('Select_pays_or_continent', 'options'),
    Output('Select_pays_or_continent', 'value'),
    Input('zone_geo', 'value'))
def update_list(zone_geo):

    list_cont_count_temp = make_fig.get_list_cont_count(zone_geo)
    return [{'label': i, 'value': i} for i in list_cont_count_temp] , []


app.run_server()
