import pandas as pd
import plotly.express as px
from sympy import EX

def get_good_df(by_sum_od_day):
    if by_sum_od_day == 'sum':
        return pd.read_csv('E:\matth\Documents\Cours\Wild code school\Data Scientist\projet\projet 5\data\sum_case\covid19_confirmed_global_sum_case.csv')
    elif  by_sum_od_day == 'by_day':
        return pd.read_csv('E:\matth\Documents\Cours\Wild code school\Data Scientist\projet\projet 5\data\case_by_day\covid19_confirmed_global_case_by_day.csv')
    else:
        return None
def make_style_fig_line_plot(df):
    try:
        fig = px.line(df)

        return fig
    except Exception as error:
        print('in make_style_fig_line_plot')

def make_good_value(df,name_col,list_col):
    try:
        for col in list_col:
            df[col] = df[col] / df[name_col]
    except Exception as error:
        print('in make_style_fig_line_plot')

def get_list_cont_count(geo='country'):
    df = get_good_df('sum')
    if geo == 'country':
        return [*list(df['continent'].unique()),*list(df['country'].unique())]
    elif 'continent':
        return list(df['continent'].unique())
    else:
        return []

def get_list_date():
    df = get_good_df('sum')
    for col in ['Unnamed: 0.1','Unnamed: 0','Internal_Row_ID','country_code']:
        if col in df.columns:
            df.drop([col],axis=1,inplace=True)
    
    columns_dates = df.select_dtypes(include=['int64']).columns

    serie_date = pd.to_datetime(df[columns_dates].T.index)
    serie_date = serie_date.to_series()
 
    new_serie = pd.Series( [serie_date[i] if i == 0 else serie_date[-1] if i == 19 else serie_date[int(len(serie_date) - (len(serie_date)/i))] for i in range(20)])
  
    return new_serie
    
def get_good_list(list_filter_geo):

    dict_country_by_continent = {
            'Asia': ['AFGHANISTAN', 'ARMENIA', 'AZERBAIJAN', 'BAHRAIN', 'BANGLADESH',
                    'BHUTAN', 'BRUNEI DARUSSALAM', 'MYANMAR', 'CAMBODIA', 'CHINA',
                    'CYPRUS', 'GEORGIA', 'INDIA', 'INDONESIA',
                    'IRAN (ISLAMIC REPUBLIC OF)', 'IRAQ', 'ISRAEL', 'JAPAN', 'JORDAN',
                    'KAZAKHSTAN', 'KOREA (REPUBLIC OF)', 'KUWAIT', 'KYRGYZSTAN',
                    "LAO PEOPLE'S DEMOCRATIC REPUBLIC", 'LEBANON', 'MALAYSIA',
                    'MALDIVES', 'MONGOLIA', 'NEPAL', 'OMAN', 'PAKISTAN', 'PHILIPPINES',
                    'QATAR', 'SAUDI ARABIA', 'SINGAPORE', 'SRI LANKA',
                    'SYRIAN ARAB REPUBLIC', 'TAIWAN, PROVINCE OF CHINA', 'TAJIKISTAN',
                    'THAILAND', 'TIMOR-LESTE', 'TURKEY', 'UNITED ARAB EMIRATES',
                    'UZBEKISTAN', 'VIET NAM', 'PALESTINE, STATE OF', 'YEMEN'],

       'Europe': ['ALBANIA', 'ANDORRA', 'AUSTRIA', 'BELARUS', 'BELGIUM',
                'BOSNIA AND HERZEGOVINA', 'BULGARIA', 'CROATIA', 'CZECH REPUBLIC',
                'DENMARK', 'ESTONIA', 'FINLAND', 'FRANCE', 'GERMANY', 'GREECE',
                'HOLY SEE', 'HUNGARY', 'ICELAND', 'IRELAND', 'ITALY',
                'MACEDONIA (THE FORMER YUGOSLAV REPUBLIC OF)', 'LATVIA',
                'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MALTA',
                'MOLDOVA (REPUBLIC OF)', 'MONACO', 'MONTENEGRO', 'NETHERLANDS',
                'NORWAY', 'POLAND', 'PORTUGAL', 'ROMANIA', 'RUSSIAN FEDERATION',
                'SAN MARINO', 'SERBIA', 'SLOVAKIA', 'SLOVENIA', 'SPAIN', 'SWEDEN',
                'SWITZERLAND', 'UKRAINE',
                'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND'],

       'Africa':['ALGERIA', 'ANGOLA', 'BENIN', 'BOTSWANA', 'BURKINA FASO',
                'BURUNDI', 'CABO VERDE', 'CAMEROON', 'CENTRAL AFRICAN REPUBLIC',
                'CHAD', 'COMOROS', 'CONGO', 'CONGO (DEMOCRATIC REPUBLIC OF THE)',
                "CÔTE D'IVOIRE", 'DJIBOUTI', 'EGYPT', 'EQUATORIAL GUINEA',
                'ERITREA', 'SWAZILAND', 'ETHIOPIA', 'GABON', 'GAMBIA', 'GHANA',
                'GUINEA', 'GUINEA-BISSAU', 'KENYA', 'LESOTHO', 'LIBERIA', 'LIBYA',
                'MADAGASCAR', 'MALAWI', 'MALI', 'MAURITANIA', 'MAURITIUS',
                'MOROCCO', 'MOZAMBIQUE', 'NAMIBIA', 'NIGER', 'NIGERIA', 'RWANDA',
                'SAO TOME AND PRINCIPE', 'SENEGAL', 'SEYCHELLES', 'SIERRA LEONE',
                'SOMALIA', 'SOUTH AFRICA', 'SOUTH SUDAN', 'SUDAN',
                'TANZANIA, UNITED REPUBLIC OF', 'TOGO', 'TUNISIA', 'UGANDA',
                'ZAMBIA', 'ZIMBABWE'],

       'Americas' : ['ANTIGUA AND BARBUDA', 'ARGENTINA', 'BAHAMAS', 'BARBADOS',
                'BELIZE', 'BOLIVIA (PLURINATIONAL STATE OF)', 'BRAZIL', 'CANADA',
                'CHILE', 'COLOMBIA', 'COSTA RICA', 'CUBA', 'DOMINICA',
                'DOMINICAN REPUBLIC', 'ECUADOR', 'EL SALVADOR', 'GRENADA',
                'GUATEMALA', 'GUYANA', 'HAITI', 'HONDURAS', 'JAMAICA', 'MEXICO',
                'NICARAGUA', 'PANAMA', 'PARAGUAY', 'PERU', 'SAINT KITTS AND NEVIS',
                'SAINT LUCIA', 'SAINT VINCENT AND THE GRENADINES', 'SURINAME',
                'TRINIDAD AND TOBAGO', 'UNITED STATES OF AMERICA', 'URUGUAY',
                'VENEZUELA (BOLIVARIAN REPUBLIC OF)'],

       'Oceania':['AUSTRALIA', 'FIJI', 'MARSHALL ISLANDS',
                'MICRONESIA (FEDERATED STATES OF)', 'NEW ZEALAND',
                'PAPUA NEW GUINEA', 'SAMOA', 'SOLOMON ISLANDS', 'VANUATU']


    }

    new_list_geo = []
    for value in list_filter_geo:
        if value in dict_country_by_continent.keys():
            for pays in dict_country_by_continent[value]:
                new_list_geo.append(pays)
        else:
            new_list_geo.append(value)
        

    return new_list_geo
def get_fig_line_plot(by_sum_or_day,geo_zone,date_end,traitement,list_filter_geo=[]):
    if list_filter_geo:
        list_filter_geo = get_good_list(list_filter_geo)
    df = get_good_df(by_sum_or_day)
    for col in ['Unnamed: 0.1','Unnamed: 0','Internal_Row_ID','country_code']:
        if col in df.columns:
            df.drop([col],axis=1,inplace=True)
    df.rename(columns={'Density (P/Km2)':'density', "Population": "population","Land Area (Km2)":'land area'},inplace=True)

    columns_dates = df.select_dtypes(include=['int64']).columns
    
  
    if geo_zone == 'country':
        df_treat = df[['population', 'continent','country','density',*columns_dates]].copy()
        df_treat = df_treat.groupby(['population', 'continent','country','density'],as_index=False).sum()
        if list_filter_geo:
            df_treat = df_treat[df_treat['country'].isin(list_filter_geo)]

    
        if traitement == 'brut':
    
            df_brut = df_treat[[ 'continent','country',*columns_dates]]
     
            df_brut=df_brut.drop('continent', axis=1).set_index('country').sort_index().T
    
            df_brut.index = pd.to_datetime(df_brut.index)
      
            df_brut = df_brut[df_brut.index < date_end]
            fig = make_style_fig_line_plot(df_brut)
            fig.update_layout(
            legend = dict(font = dict(family = "Courier", size = 6, color = "black")),
            title=f"Quantity of infection {by_sum_or_day} by country",
            xaxis_title="Date",
            yaxis_title="Quantity")
       
            return fig
        elif traitement =='population':

            columns_pop = ['population', 'continent','country']
            df_pop = df_treat[[*columns_pop,*columns_dates]]
            df_pop["population"] = df_pop["population"].str.replace(",","")
            df_pop["population"] = df_pop["population"].astype(int)
            make_good_value(df_pop,'population',columns_dates)
            df_pop = df_pop.drop(columns_pop[:2],axis=1).set_index('country').sort_index().T
            df_pop.index = pd.to_datetime(df_pop.index)
            df_pop = df_pop[df_pop.index < date_end]
            fig = make_style_fig_line_plot(df_pop)
            fig.update_layout(
            legend = dict(font = dict(family = "Courier", size = 6, color = "black")),
            title=f"Quantity of infection {by_sum_or_day} by country",
            xaxis_title="Date",
            yaxis_title="Quantity")
            return fig
        elif traitement =='density':
            columns_dens = ['density', 'continent','country']
            df_dens = df_treat[[*columns_dens,*columns_dates]]
            make_good_value(df_dens,'density',columns_dates)
            df_dens=df_dens.drop(columns_dens[:2], axis=1).set_index('country').sort_index().T
            df_dens.index = pd.to_datetime(df_dens.index)
            df_dens = df_dens[df_dens.index < date_end]
            fig = make_style_fig_line_plot(df_dens)
            fig.update_layout(
            legend = dict(font = dict(family = "Courier", size = 6, color = "black")),
            title=f"Quantity of infection {by_sum_or_day} by country",
            xaxis_title="Date",
            yaxis_title="Quantity")
            return fig
        else:
            return None
    elif geo_zone == 'continent':
    
        df_treat = df[['population','land area', 'continent','country',*columns_dates]].copy()
        df_treat["population"] = df_treat["population"].str.replace(",","")
        df_treat["population"] = df_treat["population"].astype(int)
        df_treat["land area"] = df_treat["land area"].str.replace(",","")
        df_treat["land area"] = df_treat["land area"].astype(int)
        df_treat = df_treat.groupby(['population','land area', 'continent','country'],as_index=False).sum()
        df_treat =df_treat.groupby(['continent'],as_index=False).sum()
        df_treat['density'] = df_treat['population']/df_treat['land area']
        df_treat.drop('land area',axis =1,inplace=True)
        if list_filter_geo:
            df_treat = df_treat[df_treat['continent'].isin(list_filter_geo)]

        if traitement == 'brut':
            df_brut = df_treat[[ 'continent',*columns_dates]]
            df_brut=df_brut.set_index('continent').sort_index().T
            df_brut.index = pd.to_datetime(df_brut.index)
            df_brut = df_brut[df_brut.index < date_end]
            fig = make_style_fig_line_plot(df_brut)
            fig.update_layout(
            title=f"Quantity of infection {by_sum_or_day} by continent",
            xaxis_title="Date",
            yaxis_title="Quantity")
            return fig
        elif traitement =='population':
            columns_pop = ['population', 'continent']
            df_pop = df_treat[[*columns_pop,*columns_dates]]
            make_good_value(df_pop,'population',columns_dates)
            df_pop=df_pop.drop(columns_pop[:1],axis=1).set_index('continent').sort_index().T
            df_pop.index = pd.to_datetime(df_pop.index)
            df_pop = df_pop[df_pop.index < date_end]
            fig = make_style_fig_line_plot(df_pop)
            fig.update_layout(
            title=f"Quantity of infection {by_sum_or_day} by continent",
            xaxis_title="Date",
            yaxis_title="Quantity")
            return fig

        elif traitement =='density':
            columns_dens = ['density', 'continent']
            df_dens = df_treat[[*columns_dens,*columns_dates]]
            make_good_value(df_dens,'density',columns_dates)
            df_dens=df_dens.drop(columns_dens[:1], axis=1).set_index('continent').sort_index().T
            df_dens.index = pd.to_datetime(df_dens.index)
            df_dens = df_dens[df_dens.index < date_end]
            fig = make_style_fig_line_plot(df_dens)
            fig.update_layout(
            title=f"Quantity of infection {by_sum_or_day} by continent",
            xaxis_title="Date",
            yaxis_title="Quantity")
            return fig
            

        else:
            return None
def make_map_monde(df,loc,date,range):

    fig = px.choropleth(df, 
                    locations='country',
                     locationmode ="country names",
                    color=date, # lifeExp is a column of gapminder
                    range_color = range,
                    color_continuous_scale=px.colors.sequential.OrRd)
    return fig
def make_date_to_columns(date):

    return str(f"{date.month}/{date.day}/{str(date.year)[2:]}")

def get_fig_map_monde(by_sum_or_day,geo_zone,date_end,traitement,list_filter_geo=[]):
    if traitement == 'brut':
        range_color = (0, 300000)
        if by_sum_or_day == 'sum':
            range_color= (0, 60000000)

    elif traitement == 'population':
        if geo_zone == 'continent':
            range_color = (0, 0.001)
            if by_sum_or_day == 'sum':
                range_color= (0, 0.06)
        else:
            range_color = (0, 0.001)
            if by_sum_or_day == 'sum':
                range_color= (0, 0.1)
            
    elif traitement == 'density':
        if geo_zone == 'continent':
            range_color = (0, 16000)
            if by_sum_or_day == 'sum':
                range_color= (0, 2200000)
        else:
            range_color = (0, 9500)
            if by_sum_or_day == 'sum':
                range_color= (0, 900000)
        
    
    if list_filter_geo:
        list_filter_geo = get_good_list(list_filter_geo)
    df = get_good_df(by_sum_or_day)

    for col in ['Unnamed: 0.1','Unnamed: 0','Internal_Row_ID','country_code']:
        if col in df.columns:
            df.drop([col],axis=1,inplace=True)
    df.rename(columns={'Density (P/Km2)':'density', "Population": "population","Land Area (Km2)":'land area'},inplace=True)

    columns_dates = df.select_dtypes(include=['int64']).columns

    if geo_zone == 'country':
        df_treat = df[['population', 'continent','country','density',*columns_dates]].copy()
        df_treat = df_treat.groupby(['population', 'continent','country','density'],as_index=False).sum()
        if list_filter_geo:
            df_treat = df_treat[df_treat['country'].isin(list_filter_geo)]

        if traitement == 'brut':
            df_brut = df_treat[[ 'continent','country',*columns_dates]]
            fig = make_map_monde(df_brut,'country',make_date_to_columns(date_end),range=range_color)
            return fig
        elif traitement == 'population':
            columns_pop = ['population', 'continent','country']
            df_pop = df_treat[[*columns_pop,*columns_dates]]
            df_pop["population"] = df_pop["population"].str.replace(",","")
            df_pop["population"] = df_pop["population"].astype(int)
            make_good_value(df_pop,'population',columns_dates)
            fig = make_map_monde(df_pop,'country',make_date_to_columns(date_end),range=range_color)
            return fig

        elif traitement == 'density':
            columns_dens = ['density', 'continent','country']
            df_dens = df_treat[[*columns_dens,*columns_dates]]
            make_good_value(df_dens,'density',columns_dates)
            fig = make_map_monde(df_dens,'country',make_date_to_columns(date_end),range=range_color)
            return fig
    
        else:
            return None



    elif geo_zone == 'continent':
        df_treat = df[['population','land area', 'continent','country',*columns_dates]].copy()
        df_treat["population"] = df_treat["population"].str.replace(",","")
        df_treat["population"] = df_treat["population"].astype(int)
        df_treat["land area"] = df_treat["land area"].str.replace(",","")
        df_treat["land area"] = df_treat["land area"].astype(int)
        df_treat = df_treat.groupby(['population','land area', 'continent','country'],as_index=False).sum()
        if list_filter_geo:
            df_treat = df_treat[df_treat['continent'].isin(list_filter_geo)]
        df_treat_cont =df_treat.groupby(['continent'],as_index=False).sum()
        df_treat_cont['density'] = df_treat_cont['population']/df_treat_cont['land area']
        df_treat_cont.drop('land area',axis =1,inplace=True)
    
        for col in columns_dates:
            dict_continent ={}
            for continent in df_treat_cont['continent'].unique():

                dict_continent[continent] = df_treat_cont[df_treat_cont['continent'] == continent].reset_index()[col][0]
   
            df_treat[col] = [dict_continent[x] for x in df_treat['continent']]

        df_treat['density']= df_treat['continent'].apply(lambda x : df_treat_cont[df_treat_cont['continent']==x].reset_index()['density'][0])
        df_treat['population']= df_treat['continent'].apply(lambda x : df_treat_cont[df_treat_cont['continent']==x].reset_index()['population'][0])
        if traitement == 'brut':
           
            fig = make_map_monde(df_treat,'country',make_date_to_columns(date_end),range=range_color)
            return fig

        elif traitement == 'population':

            columns_pop = ['population', 'continent','country']
            df_pop = df_treat[[*columns_pop,*columns_dates]]
            make_good_value(df_pop,'population',columns_dates)
            fig = make_map_monde(df_pop,'country',make_date_to_columns(date_end),range=range_color)
            return fig

        elif traitement == 'density':
            columns_dens = ['density', 'continent','country']
            df_dens = df_treat[[*columns_dens,*columns_dates]]
            make_good_value(df_dens,'density',columns_dates)
            fig = make_map_monde(df_dens,'country',make_date_to_columns(date_end),range=range_color)
            return fig
        else:
            return None
    else:
        return None




        

