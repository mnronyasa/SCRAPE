import streamlit as st
from turtle import width 
from mitrecve import crawler
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time 
from geopy.geocoders import Nominatim
from functools import partial
from statistics import mean
import itertools
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from streamlit_tags import st_tags
from PIL import Image
from geopy.exc import GeocoderTimedOut
import pydeck as pdk




st.set_page_config(page_title='SCRAPE',layout='wide')
image = Image.open('/Users/ronnieasatourian/Desktop/Booz Allen/logo.png')
st.image(image,width = 500,clamp = True,caption = 'By Roni Asatourian, Hunter Dolan, Alyssa Getz and Kaihil Patel')


def country_peace_score():
        url = 'https://worldpopulationreview.com/country-rankings/most-peaceful-countries'
        header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }

        page = requests.get(url,headers = header)
        soup = BeautifulSoup(page.content,'lxml')
        
        global country_peace_index
        if 'country_peace_index' not in globals():
            country_peace_index = {}

        for row in soup.find_all('table')[0].tbody.find_all('tr')[0:]:
            country_peace_index[row.find_all('td')[1].text.lower()] = float(row.find_all('td')[2].text)
        return country_peace_index

def get_global_freedom_score():
    url = 'https://freedomhouse.org/countries/freedom-world/scores'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')
    global country_territories_score
    if 'country_territories_score' not in globals():
        country_territories_score = {}
    for row in soup.find_all('tr')[1:]:
        # print(row.prettify())
        country_name = ''
        country_score = ''
        for el in row.find_all('a',href = True):
            country_name = el.text.lower()
        for el in row.find_all(class_='score'):
            country_score = el.text
        
        country_territories_score[country_name] = int(country_score)
    
    return country_territories_score

def get_political_stability_index():

    url = 'https://www.theglobaleconomy.com/rankings/wb_political_stability/'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    country_name_s = []
    score = []
    for i in soup.find_all(class_='outsideTitleElement'):
        for el in i.find_all(class_='graph_outside_link'):
            country_name_s.append(el.text.lower())

    for el in soup.find_all('div',attrs={'style':'position: absolute; top: 2px; left: 7px; height: 15px; color: #000000;'}):
        score.append(float(el.text))

    global political_stability_dict
    if 'political_stability_dict' not in globals():
        political_stability_dict = {}

    political_stability_dict = {country_name_s[i]: score[i] for i in range(len(country_name_s))}


    return political_stability_dict


def get_security_threats_index():

    url = 'https://www.theglobaleconomy.com/rankings/security_threats_index/'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    country_name_s = []
    score = []
    for i in soup.find_all(class_='outsideTitleElement'):
        for el in i.find_all(class_='graph_outside_link'):
            country_name_s.append(el.text.lower())

    for el in soup.find_all('div',attrs={'style':'position: absolute; top: 2px; left: 7px; height: 15px; color: #000000;'}):
        score.append(float(el.text))

    global political_stability_dict
    if 'political_stability_dict' not in globals():
        political_stability_dict = {}

    political_stability_dict = {country_name_s[i]: score[i] for i in range(len(country_name_s))}

    return political_stability_dict



def get_corruption_perceptions_index():

    url = 'https://www.theglobaleconomy.com/rankings/transparency_corruption/'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    country_name_s = []
    score = []

    for i in soup.find_all(class_='outsideTitleElement'):
        for el in i.find_all(class_='graph_outside_link'):
            country_name_s.append(el.text.lower())

    for el in soup.find_all('div',attrs={'style':'position: absolute; top: 2px; left: 7px; height: 15px; color: #000000;'}):
        score.append(float(el.text))

    global political_stability_dict
    if 'political_stability_dict' not in globals():
        political_stability_dict = {}

    political_stability_dict = {country_name_s[i]: score[i] for i in range(len(country_name_s))}

    return political_stability_dict



def get_country_gdp():
    url = 'https://www.worldometers.info/gdp/gdp-by-country/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content,'lxml')

    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="example2") 
    global country_gdp
    if 'country_gdp' not in globals():
        country_gdp = {}
    
    for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if(columns != []):
                gdp = columns[2].text
                gdp = ''.join([i for i in gdp if i.isdigit()])
                country_gdp[columns[1].text.lower()] = int(gdp)

    return country_gdp

def get_economic_freedom():
    url = 'https://www.heritage.org/index/ranking'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')
    country = []
    score = []

    for el in soup.find_all(class_='country'):
        if el.get_text() != 'Country':
            if el.get_text() != '':
                country.append(el.get_text(el.get_text()).lower())



    for el in soup.find_all(class_='overall'):
        if el.get_text() != 'Overall':
            if el.get_text() == 'N/A':
                score.append(1)
            else:
                score.append(float(el.get_text(el.get_text())))

    scores_dict = {country[i]:score[i] for i in range(len(score))}

    return scores_dict

def get_tariff_rate():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_tariff_rate'
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    table = soup.find_all('tr')
    country_score = {}
    for el in soup.find_all('tr')[:]:
        cells = el.find_all('td')
        if len(cells) > 1:
            country_score[cells[1].get_text()[:-1].translate({ord('\xa0'): None}).lower()] = float(cells[2].get_text()[:-3])
    return country_score


def get_natural_disaster_rate(): 
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_natural_disaster_risk'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    table = soup.find_all('tr')
    country_score = {}
    for el in soup.find_all('tr')[:]:
        cells = el.find_all('td')
        if len(cells) > 1:
            country_score[cells[1].get_text()[:-1].translate({ord('\xa0'): None}).lower().strip()] = float(cells[2].get_text()[:-2])

    return country_score



def get_fragile_states_rate(): 
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_Fragile_States_Index'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    table = soup.find_all('tr')
    country_score = {}
    for el in soup.find_all('tr')[:]:
        cells = el.find_all('td')
        if len(cells) > 1:
            res = cells[1].get_text().translate({ord('\xa0'): None}).lower().strip().replace('.', '', 1).isdigit()
            if res == False:
                country_score[cells[1].get_text().translate({ord('\xa0'): None}).lower().strip()] = float(cells[2].get_text())

    return country_score


def get_child_index():
    url = 'https://www.humanium.org/en/rcri-world-ranking-by-countries/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    page = requests.get(url,headers = header)
    soup = BeautifulSoup(page.content,'lxml')

    child_labor_index_dict = {}
    for el in soup.find_all('ol'):
        for li in el.find_all('li'): 
            if li.get_text()[:-4].strip().lower() == 'united states of america':
                child_labor_index_dict['united states'] = float(li.get_text()[-4:].strip().replace(',','.'))
            else:
                child_labor_index_dict[li.get_text()[:-4].strip().lower()] = float(li.get_text()[-4:].strip().replace(',','.'))
    return child_labor_index_dict

def calculate_nvd_risk_score(input):

    cve_info = crawler.get_main_page(input)
    cve_id = [x[0] for x in cve_info[:8]]  # for more accurate results this can loop through all the cve_ids (this only to speed up our program)

    url_lst = []
    str_score = []
    for cve in cve_id:   
        link = 'https://nvd.nist.gov/vuln/detail/'
        link += cve
        url_lst.append(link)

    score = []
    for url in url_lst: 
            # session = requests.Session()
            # adapter = HTTPAdapter(max_retries=Retry)
            # session.mount('http://', adapter)
            # session.mount('https://', adapter)

            # page = session.get(url)
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                }

            # page = requests.get(url)
            page = requests.get(url,headers = header)

            # page = requests.get(url)

            soup = BeautifulSoup(page.content,'lxml')

            for el in soup.find_all(attrs = {'class':'severityDetail'}):
                if (el.get_text()[1:5]) != '/A':
                    if (el.get_text()[1:5]) == 'N/A':
                        score.append(10.0)
                        str_score.append('10')
                    else:
                        score.append(float(el.get_text()[1:5]))
                        str_score.append(el.get_text()[1:5].strip())


    return len(cve_info),cve_id,score,str_score,url_lst

def get_company_headquarters_loc(hardware_model):
    url = 'https://www.google.com/search?hl=en&q='
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }
    new_url = ''
    company_name = hardware_model.split()[0][0:]
    new_url = url + company_name + '+company+headquarters+location'
    page = requests.get(new_url, headers=header)
    page.raise_for_status()

    soup = BeautifulSoup(page.text,'lxml')
    if soup.find('div',class_='BNeawe iBp4i AP7Wnd') is not None:
        headquarter_loc = soup.find('div',class_='BNeawe iBp4i AP7Wnd').text
    else:
        headquarter_loc = None
    
    return headquarter_loc

def get_country(loc):
    try:
        line = 0
        geolocator = Nominatim(user_agent = "get_country")
        line += 1
        geocode = partial(geolocator.geocode, language="en",timeout=15)
        line += 1
        location = str(geocode(loc))
        line += 1
    except GeocoderTimedOut as e:
        st.text(e.message)
        st.text('ERROR LINE:{}'.format(line))
    
    return location.split(',')[-1].strip().lower()



def get_travel_advisories_level(country_name):
    try:
        line = 0
        geolocator = Nominatim(user_agent = 'get_travel_advisories_level')
        geocode = partial(geolocator.geocode, language="en",timeout=15)
        line += 1
        location = str(geocode(country_name)).split(',')[-1].strip().replace(' ','')  
        if location != 'UnitedStates':
        
            url = 'https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/' + location + '.html'

            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }
            line += 1
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            line += 1
            session.mount('https://', adapter)
            line += 1
            page = session.get(url)    
            page = requests.get(url,headers = header, timeout=(2, 5))
            soup = BeautifulSoup(page.content,'lxml')
            line += 1
            travel_level = soup.find_all(class_='tsg-rwd-eab-title-frame')[1].text
            line += 1
            travel_level = int(travel_level.split(':')[0][-1]) 
        else:
            travel_level = 1
    except GeocoderTimedOut as e:
        st.text(e.message)
        st.text('ERROR LINE:{}'.format(line))

    return travel_level

def get_sanction(country):
    url = 'https://search.usa.gov/search?utf8=%E2%9C%93&affiliate=treas&query='
    url += country

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content,'lxml')
    retult = soup.find('li',{'id':'results-count'}).get_text().partition('r')[0].strip()
    if ',' in retult:
        sanction_result = float(retult.translate({ord(','):None}))
    else:
        sanction_result = float(retult)

    return sanction_result



def get_manufacturing_country(hardware_model):
    Manufacturing_data = pd.read_excel('/Users/ronnieasatourian/Desktop/Booz Allen/manufacturingCountrySheet.xlsx')
    Manufacturing_data = Manufacturing_data.replace(np.nan, '',regex=True)

    column_headers = (Manufacturing_data.columns.values.tolist())[1:] # everything besides manufacturer 

    hardware_company_name = hardware_model.split()[0][0:].lower()


    manu_country = []
    for index,row in Manufacturing_data.iterrows():
        company = row['Manufacturer']
        if company.lower() == hardware_company_name:
            for column in column_headers:
                if row[column] != '':
                    manu_country.append(row[column].lower())
            else:
                continue

    return manu_country


def get_high_tech_export(country_name):
    data = pd.read_csv('/Users/ronnieasatourian/Desktop/Booz Allen/cleaned_high_tech_export.csv')
    if (country_name in data.values) == False:
        return 0
    row_number = data.index[data['Country Name'] == country_name].tolist()[0]

    get_high_tech_export_value = data.at[row_number, '2018']
    return get_high_tech_export_value

def get_port_time(country_name):
    data = pd.read_excel('/Users/ronnieasatourian/Desktop/Booz Allen/port_times_by country.xlsx')
    data['Country'] = data['Country'].str.lower()
    if (country_name in data.values) == False:
        return 0
    row_number = data.index[data['Country'] == country_name].tolist()[0]

    port_time = data.at[row_number,'Time (days)']
    return port_time

def color_picker(score):
    return "red" if score >= 7.0 else "green" if score < 4.0 else 'orange'

def risk_generator(data,index,field_names):
    scores = [country[index] for country in data]

    colored_scores = ''
    for i,score in enumerate(scores):
        if(i == 0):
            colored_scores = '<span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)
        else:
            colored_scores += ', <span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)       
    st.markdown('{}: **{}**'.format(field_names[index],colored_scores), unsafe_allow_html=True) 

def tot_metric_picker(label,score):
    if score < 4.0:
        st.metric(label= label, value= score, delta='Low') 
    if score < 7.0 and score >= 4.0:
        st.metric(label= label, value= score, delta='Med',delta_color='off') 
    if score >= 7.0:
        st.metric(label= label, value= score, delta='High',delta_color='inverse') 

def get_political_risk_more_info():
    st.info('**A scale from 1 to 10 is used for all calculations (1 being the lowest score and 10 the highest score)**')
    st.info('**Freedom Score:** Freedom House - a measure of countries relative rank of citizens\' civil liberties and rights' )
    st.info('**Peace Score:** Institute for Economics and Peace - measures the relative position of nation\'s and region\'s peacefulness' )
    st.info('**Travel Advisory:** U.S. State Department - Risk of traveling to countries from the Unites States on a scale of 1-4' )
    st.info('**Political Stability:** The Global Economy -  the likelihood that a government will be destabilized or overthrown by unconstitutional or violent means' )
    st.info('**Security Threat:** The Global Economy - a score of the physical and technological threat a country poses to the United States and its citizens' )
    st.info('**Corruption Index:** The Global Economy - ranks countries by their perceived levels of public sector corruption, including the government' )
    st.info('**GDP:** World Bank OECD - Gross Domestic Product, a monetary measure of the market value of all goods and services produced by countries' )

def get_security_risk_more_info():
    st.info('**A scale from 1 to 10 is used for all calculations (1 being the lowest score and 10 the highest score)**')
    st.info('**NVD Score:** National Vulnerability Database - compiled list of publicly known cybersecurity vulnerabilities (CVE)' )

def get_economic_risk_more_info():
    st.info('**A scale from 1 to 10 is used for all calculations (1 being the lowest score and 10 the highest score)**')
    st.info('**Economic Freedom Score:** Heritage - The ability to work, produce, consume, and invest  in ones own labor and property in a country')
    st.info('**Tarrif Score:** Wikipedia - Export tariff rates by country into the United States')
    st.info('**Sanction Score:** U.S. Department of the Treasury - the number of economic sanctions the Unites States has placed against a country')
    st.info('**Embargo Score:** U.S. Department of the Treasury - list of counties the United States does not purchase goods from due to high risk')

def get_production_risk_more_info():
    st.info('**A scale from 1 to 10 is used for all calculations (1 being the lowest score and 10 the highest score)**')
    st.info('**Natural Disaster Score:** RUHR University World Report - countries ranked by risk of natural disaster')
    st.info('**Fragile State Score:** Foreign Policy: Fragile States Index Report - countries with characteristics that substantially impair their economic and social performance such as war, government, and social tension')
    st.info('**Children In Employment Score:** Humanium - Percent of children in employment, often in unsafe and unlawful working conditions')
    st.info('**Product Export Score:** World Bank - Countries with a high percentage of technological exports are said to be more reliable to manufacture electronic products')
    st.info('**Port Time Score:** Statista - Average amount of time that a cargo ship is docked in a country\'s port')

def get_lat_long(loc):
    try:
        line = 0
        geolocator = Nominatim(user_agent='SCRAPE')
        line += 1
        location = geolocator.geocode(loc,timeout=15)
        line += 1
    except GeocoderTimedOut as e:
        st.text(e.message)
        st.text('ERROR LINE:{}'.format(line))

    return location.latitude,location.longitude 

def set_map(head_latitude,head_longitude):
  data2 = np.random.randn(1, 1) / [250, 250] + [head_latitude ,head_longitude]     
  df = pd.DataFrame(
  data2,
  columns=['lat', 'lon'])

  st.pydeck_chart(pdk.Deck(
              map_style='mapbox://styles/mapbox/light-v9',
              initial_view_state=pdk.ViewState(
                  latitude=head_latitude,
                  longitude=head_longitude,
                  zoom=8,
                  height=600,
                  width=1725
              ),
              layers=[
                  pdk.Layer(
                      'ScatterplotLayer',
                      data=df,
                      get_position='[lon, lat]',
                      get_color='[200, 30, 0, 160]',
                      get_radius=6000,
                      auto_highlight=True
                  ),
              ],
          ))

embargo_countries = ['iran','north korea','syria','sudan','cuba','russia','venezuela']
my_bar = st.progress(0)

get_global_freedom_score_dict = get_global_freedom_score()

my_bar.progress(20)
country_peace_score_dict = country_peace_score()
get_political_stability_index_dict = get_political_stability_index()
my_bar.progress(40)
get_security_threats_index_dict = get_security_threats_index()
get_corruption_perceptions_index_dict = get_corruption_perceptions_index()

get_natural_disaster_rate_dict = get_natural_disaster_rate()
get_fragile_states_rate_dict = get_fragile_states_rate()
get_child_index_dict = get_child_index()

my_bar.progress(80)
get_country_gdp_dict = get_country_gdp()

get_economic_freedom_dict = get_economic_freedom()
get_tariff_rate_dict = get_tariff_rate()
my_bar.progress(100)
#####################################################################
#####################################################################
#####################################################################
#####################################################################
########################     GPU      ###############################
########################     GPU      ###############################
########################     GPU      ###############################
########################     GPU      ###############################
########################     GPU      ###############################
########################     GPU      ###############################
#####################################################################
#####################################################################
#####################################################################


with st.form('gpu'):
    col1,col2 = st.columns([1,1.3])
    with col2:
        submitted_2 = st.form_submit_button('Calculate GPU Risks')
    if submitted_2:

        with st.spinner('SCRAPE Is Looking For GPU Risk 😎'):
            

            gpu_url = 'https://www.gpucheck.com/graphics-cards'
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }
            page = requests.get(gpu_url, headers=header)

            soup = BeautifulSoup(page.content,'lxml')

            gpu_names = {el.get_text().lower() for el in soup.find_all('strong')} #using set o(1) for better performance

            def val_gpu(input):
                gpu_set = gpu_names
                if input not in gpu_set:
                    return False
                return True

            def get_input_gpu():

                gpu_name = st_tags(
                    label='GPU',
                    text='Press enter to add your GPU model',
                    suggestions=list(gpu_names),
                    value=['NVIDIA GeForce RTX 3090'],
                    maxtags = 1,
                    key='1')
                

                if not val_gpu(gpu_name[0].lower()):
                    st.error('No match has been detected enter your graphics card again')
                    st.stop()
                st.success('Valid GPU')       

                    
                return gpu_name[0]
                



            gpu_input = get_input_gpu()
            company_name = gpu_input.split()[0][0:]
            headquarters_location = get_company_headquarters_loc(gpu_input)
            headquarters_country = get_country(get_company_headquarters_loc(gpu_input))
            manufacturer_counties = get_manufacturing_country(gpu_input)

            
            countries = []
            if (headquarters_country in manufacturer_counties) == False:
                countries.extend(manufacturer_counties)
                countries.append(headquarters_country)
            else:
                countries.extend(manufacturer_counties)
            
            headquarters_global_freedom_score = 0
            headquarters_peace_score = 0
            headquarters_travel_advisory_score = 0
            headquarters_political_stability_score = 0
            headquarters_security_threats_score = 0
            headquarters_corruption_score = 0
            headquarters_gdp_score = 0


            headquarters_economic_freedom_score = 0
            headquarters_tarrif_score = 0
            headquarters_sanction_score = 0
            headquarters_embargo_score = 0

            headquarters_natural_disaster_score = 0
            headquarters_fragile_states_rate = 0
            headquarters_child_index_rate = 0
            headquarters_high_tech_export_rate = 0
            headquarters_port_time = 0
            

            global_freedom_score = 0
            peace_score = 0
            travel_advisory_score = 0
            political_stability_score = 0
            security_threats_score = 0
            corruption_score = 0
            gdp_score = 0

            economic_freedom_score = 0
            tarrif_score = 0
            sanction_score = 0
            embargo_score = 0

            natural_disaster_score = 0
            fragile_states_rate = 0
            child_index_rate = 0
            high_tech_export_rate = 0
            port_time = 0

            info = {'headquarters':[],'manufacturer':[]}
            economic_info = {'headquarters':[],'manufacturer':[]}
            production_info = {'headquarters':[],'manufacturer':[]}
            

            for country in countries:
                if country == headquarters_country:
                    headquarters_global_freedom_score = round((10-get_global_freedom_score_dict.get(country)/10),2)
                    headquarters_peace_score =  round((country_peace_score_dict.get(country)*2),2)

                    headquarters_travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)
                    
                    headquarters_economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        headquarters_tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        headquarters_tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)

                    if country == 'united states':
                        headquarters_sanction_score = 0
                    else:
                            headquarters_sanction_score = round(((get_sanction(country) / 1000) * 4),2)

                    if (country in embargo_countries) == True:
                        headquarters_embargo_score = 10
                    else:
                        headquarters_embargo_score = 0

                    headquarters_political_stability_score = 0
                    headquarters_security_threats_score = 0
                    headquarters_corruption_score = 0
                    if country == 'united states':
                        country_temp = 'usa'
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country_temp)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)


                    headquarters_gdp_score = 0 
                    if country in get_country_gdp_dict:
                        # headquarters_gdp_score = get_country_gdp_dict.get(country)
                        headquarters_gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        headquarters_gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)

                    headquarters_natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        headquarters_natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        headquarters_natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    headquarters_fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        headquarters_fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        headquarters_fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    headquarters_child_index_rate = 0
                    if country in get_child_index_dict:
                        headquarters_child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        headquarters_child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    headquarters_high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    headquarters_port_time = round((get_port_time(country) * 2),2)

                    info['headquarters'].append([country,headquarters_global_freedom_score,headquarters_peace_score,headquarters_travel_advisory_score,headquarters_political_stability_score,headquarters_security_threats_score,headquarters_corruption_score,headquarters_gdp_score])
                    economic_info['headquarters'].append([country,headquarters_economic_freedom_score,headquarters_tarrif_score,headquarters_sanction_score,headquarters_embargo_score])
                    production_info['headquarters'].append([country,headquarters_natural_disaster_score,headquarters_fragile_states_rate,headquarters_child_index_rate,headquarters_high_tech_export_rate,headquarters_port_time])
                else:
                    global_freedom_score = round(10-(get_global_freedom_score_dict.get(country)/10),2)
                    peace_score = round((country_peace_score_dict.get(country)*2),2)

                    travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)

                    economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)
                    
                    if country == 'united states':
                        sanction_score = 0
                    else:
                        sanction_score = round(((get_sanction(country) / 1000) * 4),2)
                    
                    if (country in embargo_countries) == True:
                        embargo_score = 10
                    else:
                        embargo_score = 0

                    political_stability_score = 0
                    security_threats_score = 0
                    corruption_score = 0
                    if country.lower() == 'united states':
                        country_temp = 'usa'
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        security_threats_score = get_security_threats_index_dict.get(country_temp)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)

            
                    gdp_score = 0 
                    if country in get_country_gdp_dict:
                        gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)


            
                    natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    child_index_rate = 0
                    if country in get_child_index_dict:
                        child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    port_time = round((get_port_time(country) * 2),2)

                    info['manufacturer'].append([country,global_freedom_score,peace_score,travel_advisory_score,political_stability_score,security_threats_score,corruption_score,gdp_score])
                    economic_info['manufacturer'].append([country,economic_freedom_score,tarrif_score,sanction_score,embargo_score])
                    production_info['manufacturer'].append([country,natural_disaster_score,fragile_states_rate,child_index_rate,high_tech_export_rate,port_time])

            
            
            head_score_list = ([score[1:] for score in info['headquarters']]) 
            headquarters_political_risk_score = round(mean(list(itertools.chain(*head_score_list))),2)
            manu_score_list = ([score[1:] for score in info['manufacturer']]) 
            manu_political_risk_score = round(mean(list(itertools.chain(*manu_score_list))),2)
            
            total_political_risk_score = round((headquarters_political_risk_score + manu_political_risk_score)/2,2)
            
            head_score_economic_list = ([score[1:] for score in economic_info['headquarters']]) 
            headquarters_economic_risk_score = round(mean(list(itertools.chain(*head_score_economic_list))),2)
            manu__economic_score_list = ([score[1:] for score in economic_info['manufacturer']]) 
            manu_economic_risk_score = round(mean(list(itertools.chain(*manu__economic_score_list))),2)

            total_economic_risk_score = round((headquarters_economic_risk_score + manu_economic_risk_score)/2,2)


            head_score_production_list = ([score[1:] for score in production_info['headquarters']]) 
            headquarters_production_risk_score = round(mean(list(itertools.chain(*head_score_production_list))),2)
            manu__production_score_list = ([score[1:] for score in production_info['manufacturer']]) 
            manu_production_risk_score = round(mean(list(itertools.chain(*manu__production_score_list))),2)

            total_production_risk_score = round((headquarters_production_risk_score + manu_production_risk_score)/2,2)            

            political_agree_column,Security_risk_agree_column,economic_risk_agree_column,production_risk_agree_column = st.columns([1,1,1,1])
            with political_agree_column:
                political_risk_agree = st.checkbox('Get More Political Risk Info',key="1")
                if political_risk_agree:
                    get_political_risk_more_info()
            with Security_risk_agree_column:
                Security_risk_agree = st.checkbox('Get More Security Risk Info',key="2")
                if Security_risk_agree:
                    get_security_risk_more_info()
            with economic_risk_agree_column:
                economic_risk_agree = st.checkbox('Get More Economic Risk Info',key="3")    
                if economic_risk_agree:
                    get_economic_risk_more_info()
            with production_risk_agree_column:
                production_risk_agree = st.checkbox('Get More Production Risk Info',key="4")  
                if production_risk_agree:
                    get_production_risk_more_info()

            political_headquart_col, political_manufac_col,security_score = st.columns([1,2,3])
            
            with political_headquart_col:
                st.header('Political Risk')
                st.subheader('Headquarters:')

                political_risks_types = ['Country','Freedom Score','Peace Score','Travel Advisory','Political Stability','Security Threat','Corruption Index','GDP']

                headquarter_country_list = [country[0] for country in info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(headquarter_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['headquarters'],i,political_risks_types)

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(headquarters_political_risk_score),headquarters_political_risk_score)
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

                    
            with political_manufac_col:
                for i in range(5):
                    st.text('')
            
                st.subheader('Manufacturers:')
                
                manu_country_list = [country[0] for country in info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(manu_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['manufacturer'],i,political_risks_types)
                
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_political_risk_score,2)),round(manu_political_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                


            nvd_tot_results,cve_id,scores,str_score,url_list = calculate_nvd_risk_score(gpu_input)
            with security_score:
                st.header('Security Risk')
                
                st.subheader('{} CVE IDs Available'.format(nvd_tot_results))
                st.warning('Since SCRAPE restricts the amount of CVE IDs utilized owing to program performance, only 8 CVE IDs will be used in the computations. For future editions, this can be changed for more accurate results.')
                st.subheader('CVE ID:')

                cve_hyper = ''
                for i,id in enumerate(cve_id):
                    if(i == 0):
                        cve_hyper = '[{}]({})'.format(id,url_list[i])
                    else:
                        cve_hyper += ', [{}]({})'.format(id,url_list[i])
                        
                st.write(cve_hyper)
                colored_cve_scores = ''
                for i,score in enumerate(scores):
                    if(i == 0):
                        colored_cve_scores = '<span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)
                    else:
                        colored_cve_scores += ', <span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)       
                st.subheader('Scores: ')
                st.markdown('**{}**'.format(colored_cve_scores), unsafe_allow_html=True)
            cve_tot_score = round(mean(scores),2)
            st.text('')


            economic_headquartes_risk_score,economic_manufac_risk_score,production_headquarters_risk_score,production_manufac_risk_score = st.columns([1,2,1,2])
            
            with economic_headquartes_risk_score:

                st.header('Economic Risk')

                st.subheader('Headquarters:')

                economic_headquarter_country_list = [country[0] for country in economic_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(economic_headquarter_country_list)))

                
                economic_risks_types = ['Country','Economic Freedom Score','Tarrif Score','Sanction Score','Embargo Score']
                
                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['headquarters'],i,economic_risks_types)  


                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_economic_risk_score,2)),round(headquarters_economic_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with economic_manufac_risk_score:
                for i in range(5):
                    st.text('')
                
                st.subheader('Manufacturers:')
                econonic_manu_country_list = [country[0] for country in economic_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(econonic_manu_country_list)))

                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['manufacturer'],i,economic_risks_types)  

                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_economic_risk_score,2)),round(manu_economic_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with production_headquarters_risk_score:

                st.header('Production Risk')
                st.subheader('Headquarters:')
                
                production_risks_types = ['Country','Natural Disaster Score','Fragile State Score','Children In Employment Score','Product Export Score','Port Time Score']
                production_headquarter_country_list = [country[0] for country in production_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(production_headquarter_country_list)))
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['headquarters'],i,production_risks_types)  

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_production_risk_score,2)),round(headquarters_production_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 

        
            with production_manufac_risk_score:
                for i in range(5):
                    st.text('')

                st.subheader('Manufacturers:')                

                production_manufac_country_list = [country[0] for country in production_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(' '.join(production_manufac_country_list)))
                # ***** FIX CAPITALIZE LATER ********** 
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['manufacturer'],i,production_risks_types)    
        
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_production_risk_score,2)),round(manu_production_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 


    ########## Total column calculation #########################

        for i in range(4):
            st.text('')
        c1,c2 = st.columns([1,1.35])
        with c2:
            st.title('Total Risks')
        colT5,colT1,colT2, colT3,colT4,colT6 = st.columns([3,1,1,1,1,3])


        with colT1:
            tot_metric_picker('Political Risk Score',total_political_risk_score)
        with colT2:
            tot_metric_picker('Security Risk Score',cve_tot_score)
        with colT3:
            tot_metric_picker('Economic Risk Score',total_economic_risk_score)
        with colT4:
            tot_metric_picker('Production Risk Score',total_production_risk_score)


        bar_graph,a,b = st.columns([0.7,2,1])
        with a:
            for i in range(2):
                st.text('')    
                
            data = {'Political':total_political_risk_score, 'Security':cve_tot_score, 'Economic': total_economic_risk_score, 'Production':total_production_risk_score}
            risk_type = list(data.keys())
            values = list(data.values())
            colors = ["red" if i >= 7.0 else "green" if i < 4.0 else 'orange' for i in values]
            fig = plt.figure(figsize = (8, 4))
            leg_colors = {'High':'red', 'Medium':'orange','Low':'green'}         
            labels = list(leg_colors.keys())
            handles = [plt.Rectangle((0,0),1,1, color=leg_colors[label]) for label in labels]
            plt.legend(handles,labels)

            plt.bar(risk_type, values,color=colors)
            plt.xlabel("Risk Type",fontsize=10)
            plt.ylabel("Risk Score",fontsize=10)
            plt.rcParams.update({'font.size': 6})
            st.pyplot(fig)

        
        for i in range(3):
            st.text('')
            
        st.markdown('### **{}** Headquarters Location: **_{}_**'.format(company_name.capitalize(),headquarters_location))
         
        head_latitude, head_longitude = get_lat_long(headquarters_location)       
        set_map(head_latitude,head_longitude)
    
    
            
#####################################################################
#####################################################################
#####################################################################
#####################################################################
########################     CPU      ###############################
########################     CPU      ###############################
########################     CPU      ###############################
########################     CPU      ###############################
########################     CPU      ###############################
########################     CPU      ###############################
#####################################################################
#####################################################################
#####################################################################

with st.form('cpu'):
    col1,col2 = st.columns([1,1.3])
    with col2:
        submitted_2 = st.form_submit_button('Calculate CPU Risks')
    if submitted_2:

        with st.spinner('SCRAPE Is Looking For CPU Risk 😎'):
            

            cpu_url = 'https://www.cpubenchmark.net/cpu_list.php'
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }
            page = requests.get(cpu_url, headers=header)
            soup = BeautifulSoup(page.content,'lxml')

            table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="cputable") 

            cpu_names = set()
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')

                if(columns != []):
                    cpu_names.add(columns[0].text.strip().lower())



            def val_cpu(input):
                cpu_set = cpu_names
                if input not in cpu_set:
                    return False
                return True
           
            def get_input_cpu():
                
                # cpu_name = list(st.text_input('cpu'))
                cpu_name = st_tags(
                    label='CPU',
                    text='Press enter to add your CPU model',
                    suggestions=list(cpu_names),
                    value=['Apple M1 Pro 10 Core 3200 MHz'],
                    maxtags = 1,
                    key='1')
                

                if not val_cpu(cpu_name[0].lower()):
                    st.error('No match has been detected enter your CPU again')
                    st.stop()
                st.success('Valid CPU')       

                          
                return cpu_name[0]
                



            cpu_input = get_input_cpu()
            company_name = cpu_input.split()[0][0:]
            headquarters_location = get_company_headquarters_loc(cpu_input)
            headquarters_country = get_country(get_company_headquarters_loc(cpu_input))
            manufacturer_counties = get_manufacturing_country(cpu_input)

            
            countries = []
            if (headquarters_country in manufacturer_counties) == False:
                countries.extend(manufacturer_counties)
                countries.append(headquarters_country)
            else:
                countries.extend(manufacturer_counties)
            
            headquarters_global_freedom_score = 0
            headquarters_peace_score = 0
            headquarters_travel_advisory_score = 0
            headquarters_political_stability_score = 0
            headquarters_security_threats_score = 0
            headquarters_corruption_score = 0
            headquarters_gdp_score = 0


            headquarters_economic_freedom_score = 0
            headquarters_tarrif_score = 0
            headquarters_sanction_score = 0
            headquarters_embargo_score = 0

            headquarters_natural_disaster_score = 0
            headquarters_fragile_states_rate = 0
            headquarters_child_index_rate = 0
            headquarters_high_tech_export_rate = 0
            headquarters_port_time = 0
            

            global_freedom_score = 0
            peace_score = 0
            travel_advisory_score = 0
            political_stability_score = 0
            security_threats_score = 0
            corruption_score = 0
            gdp_score = 0

            economic_freedom_score = 0
            tarrif_score = 0
            sanction_score = 0
            embargo_score = 0

            natural_disaster_score = 0
            fragile_states_rate = 0
            child_index_rate = 0
            high_tech_export_rate = 0
            port_time = 0

            info = {'headquarters':[],'manufacturer':[]}
            economic_info = {'headquarters':[],'manufacturer':[]}
            production_info = {'headquarters':[],'manufacturer':[]}
            

            for country in countries:
                if country == headquarters_country:
                    headquarters_global_freedom_score = round((10-get_global_freedom_score_dict.get(country)/10),2)
                    headquarters_peace_score =  round((country_peace_score_dict.get(country)*2),2)

                    headquarters_travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)
                    
                    headquarters_economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        headquarters_tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        headquarters_tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)

                    if country == 'united states':
                        headquarters_sanction_score = 0
                    else:
                            headquarters_sanction_score = round(((get_sanction(country) / 1000) * 4),2)

                    if (country in embargo_countries) == True:
                        headquarters_embargo_score = 10
                    else:
                        headquarters_embargo_score = 0

                    headquarters_political_stability_score = 0
                    headquarters_security_threats_score = 0
                    headquarters_corruption_score = 0
                    if country == 'united states':
                        country_temp = 'usa'
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country_temp)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)


                    headquarters_gdp_score = 0 
                    if country in get_country_gdp_dict:
                        # headquarters_gdp_score = get_country_gdp_dict.get(country)
                        headquarters_gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        headquarters_gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)

                    headquarters_natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        headquarters_natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        headquarters_natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    headquarters_fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        headquarters_fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        headquarters_fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    headquarters_child_index_rate = 0
                    if country in get_child_index_dict:
                        headquarters_child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        headquarters_child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    headquarters_high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    headquarters_port_time = round((get_port_time(country) * 2),2)

                    info['headquarters'].append([country,headquarters_global_freedom_score,headquarters_peace_score,headquarters_travel_advisory_score,headquarters_political_stability_score,headquarters_security_threats_score,headquarters_corruption_score,headquarters_gdp_score])
                    economic_info['headquarters'].append([country,headquarters_economic_freedom_score,headquarters_tarrif_score,headquarters_sanction_score,headquarters_embargo_score])
                    production_info['headquarters'].append([country,headquarters_natural_disaster_score,headquarters_fragile_states_rate,headquarters_child_index_rate,headquarters_high_tech_export_rate,headquarters_port_time])
                else:
                    global_freedom_score = round(10-(get_global_freedom_score_dict.get(country)/10),2)
                    peace_score = round((country_peace_score_dict.get(country)*2),2)

                    travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)

                    economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)
                    
                    if country == 'united states':
                        sanction_score = 0
                    else:
                        sanction_score = round(((get_sanction(country) / 1000) * 4),2)
                    
                    if (country in embargo_countries) == True:
                        embargo_score = 10
                    else:
                        embargo_score = 0

                    political_stability_score = 0
                    security_threats_score = 0
                    corruption_score = 0
                    if country.lower() == 'united states':
                        country_temp = 'usa'
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        security_threats_score = get_security_threats_index_dict.get(country_temp)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)

            
                    gdp_score = 0 
                    if country in get_country_gdp_dict:
                        gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)


            
                    natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    child_index_rate = 0
                    if country in get_child_index_dict:
                        child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    port_time = round((get_port_time(country) * 2),2)

                    info['manufacturer'].append([country,global_freedom_score,peace_score,travel_advisory_score,political_stability_score,security_threats_score,corruption_score,gdp_score])
                    economic_info['manufacturer'].append([country,economic_freedom_score,tarrif_score,sanction_score,embargo_score])
                    production_info['manufacturer'].append([country,natural_disaster_score,fragile_states_rate,child_index_rate,high_tech_export_rate,port_time])

            
            
            head_score_list = ([score[1:] for score in info['headquarters']]) 
            headquarters_political_risk_score = round(mean(list(itertools.chain(*head_score_list))),2)
            manu_score_list = ([score[1:] for score in info['manufacturer']]) 
            manu_political_risk_score = round(mean(list(itertools.chain(*manu_score_list))),2)
            
            total_political_risk_score = round((headquarters_political_risk_score + manu_political_risk_score)/2,2)
            
            head_score_economic_list = ([score[1:] for score in economic_info['headquarters']]) 
            headquarters_economic_risk_score = round(mean(list(itertools.chain(*head_score_economic_list))),2)
            manu__economic_score_list = ([score[1:] for score in economic_info['manufacturer']]) 
            manu_economic_risk_score = round(mean(list(itertools.chain(*manu__economic_score_list))),2)

            total_economic_risk_score = round((headquarters_economic_risk_score + manu_economic_risk_score)/2,2)


            head_score_production_list = ([score[1:] for score in production_info['headquarters']]) 
            headquarters_production_risk_score = round(mean(list(itertools.chain(*head_score_production_list))),2)
            manu__production_score_list = ([score[1:] for score in production_info['manufacturer']]) 
            manu_production_risk_score = round(mean(list(itertools.chain(*manu__production_score_list))),2)

            total_production_risk_score = round((headquarters_production_risk_score + manu_production_risk_score)/2,2)            

            political_agree_column,Security_risk_agree_column,economic_risk_agree_column,production_risk_agree_column = st.columns([1,1,1,1])
            with political_agree_column:
                political_risk_agree = st.checkbox('Get More Political Risk Info',key="1")
                if political_risk_agree:
                    get_political_risk_more_info()
            with Security_risk_agree_column:
                Security_risk_agree = st.checkbox('Get More Security Risk Info',key="2")
                if Security_risk_agree:
                    get_security_risk_more_info()
            with economic_risk_agree_column:
                economic_risk_agree = st.checkbox('Get More Economic Risk Info',key="3")    
                if economic_risk_agree:
                    get_economic_risk_more_info()
            with production_risk_agree_column:
                production_risk_agree = st.checkbox('Get More Production Risk Info',key="4")  
                if production_risk_agree:
                    get_production_risk_more_info()

            political_headquart_col, political_manufac_col,security_score = st.columns([1,2,3])
            
            with political_headquart_col:
                st.header('Political Risk')
                st.subheader('Headquarters:')

                political_risks_types = ['Country','Freedom Score','Peace Score','Travel Advisory','Political Stability','Security Threat','Corruption Index','GDP']

                headquarter_country_list = [country[0] for country in info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(headquarter_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['headquarters'],i,political_risks_types)

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(headquarters_political_risk_score),headquarters_political_risk_score)
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

                    
            with political_manufac_col:
                for i in range(5):
                    st.text('')
            
                st.subheader('Manufacturers:')
                
                manu_country_list = [country[0] for country in info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(manu_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['manufacturer'],i,political_risks_types)
                
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_political_risk_score,2)),round(manu_political_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                


            nvd_tot_results,cve_id,scores,str_score,url_list = calculate_nvd_risk_score(cpu_input)
            with security_score:
                st.header('Security Risk')
                
                st.subheader('{} CVE IDs Available'.format(nvd_tot_results))
                st.warning('Since SCRAPE restricts the amount of CVE IDs utilized owing to program performance, only 8 CVE IDs will be used in the computations. For future editions, this can be changed for more accurate results.')
                st.subheader('CVE ID:')

                cve_hyper = ''
                for i,id in enumerate(cve_id):
                    if(i == 0):
                        cve_hyper = '[{}]({})'.format(id,url_list[i])
                    else:
                        cve_hyper += ', [{}]({})'.format(id,url_list[i])
                        
                st.write(cve_hyper)
                colored_cve_scores = ''
                for i,score in enumerate(scores):
                    if(i == 0):
                        colored_cve_scores = '<span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)
                    else:
                        colored_cve_scores += ', <span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)       
                st.subheader('Scores: ')
                st.markdown('**{}**'.format(colored_cve_scores), unsafe_allow_html=True)
            cve_tot_score = round(mean(scores),2)
            st.text('')


            economic_headquartes_risk_score,economic_manufac_risk_score,production_headquarters_risk_score,production_manufac_risk_score = st.columns([1,2,1,2])
            
            with economic_headquartes_risk_score:

                st.header('Economic Risk')

                st.subheader('Headquarters:')

                economic_headquarter_country_list = [country[0] for country in economic_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(economic_headquarter_country_list)))

                
                economic_risks_types = ['Country','Economic Freedom Score','Tarrif Score','Sanction Score','Embargo Score']
                
                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['headquarters'],i,economic_risks_types)  


                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_economic_risk_score,2)),round(headquarters_economic_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with economic_manufac_risk_score:
                for i in range(5):
                    st.text('')
                
                st.subheader('Manufacturers:')
                econonic_manu_country_list = [country[0] for country in economic_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(econonic_manu_country_list)))

                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['manufacturer'],i,economic_risks_types)  

                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_economic_risk_score,2)),round(manu_economic_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with production_headquarters_risk_score:

                st.header('Production Risk')
                st.subheader('Headquarters:')
                
                production_risks_types = ['Country','Natural Disaster Score','Fragile State Score','Children In Employment Score','Product Export Score','Port Time Score']
                production_headquarter_country_list = [country[0] for country in production_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(production_headquarter_country_list)))
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['headquarters'],i,production_risks_types)  

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_production_risk_score,2)),round(headquarters_production_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 

        
            with production_manufac_risk_score:
                for i in range(5):
                    st.text('')

                st.subheader('Manufacturers:')                

                production_manufac_country_list = [country[0] for country in production_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(' '.join(production_manufac_country_list)))
                # ***** FIX CAPITALIZE LATER ********** 
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['manufacturer'],i,production_risks_types)    
        
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_production_risk_score,2)),round(manu_production_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 


    ########## Total column calculation #########################

        for i in range(4):
            st.text('')
        c1,c2 = st.columns([1,1.35])
        with c2:
            st.title('Total Risks')
        colT5,colT1,colT2, colT3,colT4,colT6 = st.columns([3,1,1,1,1,3])


        with colT1:
            tot_metric_picker('Political Risk Score',total_political_risk_score)
        with colT2:
            tot_metric_picker('Security Risk Score',cve_tot_score)
        with colT3:
            tot_metric_picker('Economic Risk Score',total_economic_risk_score)
        with colT4:
            tot_metric_picker('Production Risk Score',total_production_risk_score)



            

        bar_graph,a,b = st.columns([0.7,2,1])
        with a:
            for i in range(2):
                st.text('')    
                
            data = {'Political':total_political_risk_score, 'Security':cve_tot_score, 'Economic': total_economic_risk_score, 'Production':total_production_risk_score}
            risk_type = list(data.keys())
            values = list(data.values())
            colors = ["red" if i >= 7.0 else "green" if i < 4.0 else 'orange' for i in values]
            fig = plt.figure(figsize = (8, 4))
            leg_colors = {'High':'red', 'Medium':'orange','Low':'green'}         
            labels = list(leg_colors.keys())
            handles = [plt.Rectangle((0,0),1,1, color=leg_colors[label]) for label in labels]
            plt.legend(handles,labels)

            plt.bar(risk_type, values,color=colors)
            plt.xlabel("Risk Type",fontsize=10)
            plt.ylabel("Risk Score",fontsize=10)
            plt.rcParams.update({'font.size': 6})
            st.pyplot(fig)

        
        for i in range(3):
            st.text('')
            
        st.markdown('### **{}** Headquarters Location: **_{}_**'.format(company_name.capitalize(),headquarters_location))
         
        head_latitude, head_longitude = get_lat_long(headquarters_location)       
        set_map(head_latitude,head_longitude)

        


#####################################################################
#####################################################################
#####################################################################
#####################################################################
########################     RAM      ###############################
########################     RAM      ###############################
########################     RAM      ###############################
########################     RAM      ###############################
########################     RAM      ###############################
########################     RAM      ###############################
#####################################################################
#####################################################################
#####################################################################

with st.form('RAM'):
    col1,col2 = st.columns([1,1.3])
    with col2:
        submitted_2 = st.form_submit_button('Calculate RAM Risks')
    if submitted_2:

        with st.spinner('SCRAPE Is Looking For RAM Risk 😎'):
            

            ram_url = 'https://www.memorybenchmark.net/ram_list-ddr4.php'
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }

            page = requests.get(ram_url,headers = header)
            soup = BeautifulSoup(page.content,'lxml')
            table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="cputable")

            ram_names = set()
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if(columns != []):
                    ram_names.add(columns[0].text.strip().lower())




            def val_ram(input):
                ram_set = ram_names
                if input not in ram_set:
                    return False
                return True
           
            def get_input_ram():
                
                # ram_name = list(st.text_input('ram'))
                ram_name = st_tags(
                    label='RAM',
                    text='Press enter to add your ram model',
                    suggestions=list(ram_names),
                    value=['Samsung 8G2666CL19 8GB'],
                    maxtags = 1,
                    key='1')
                

                if not val_ram(ram_name[0].lower()):
                    st.error('No match has been detected enter your RAM again')
                    st.stop()
                st.success('Valid RAM')       

                          
                return ram_name[0]
                



            ram_input = get_input_ram()
            company_name = ram_input.split()[0][0:]
            headquarters_location = get_company_headquarters_loc(ram_input)
            headquarters_country = get_country(get_company_headquarters_loc(ram_input))
            manufacturer_counties = get_manufacturing_country(ram_input)

            
            countries = []
            if (headquarters_country in manufacturer_counties) == False:
                countries.extend(manufacturer_counties)
                countries.append(headquarters_country)
            else:
                countries.extend(manufacturer_counties)
            
            headquarters_global_freedom_score = 0
            headquarters_peace_score = 0
            headquarters_travel_advisory_score = 0
            headquarters_political_stability_score = 0
            headquarters_security_threats_score = 0
            headquarters_corruption_score = 0
            headquarters_gdp_score = 0


            headquarters_economic_freedom_score = 0
            headquarters_tarrif_score = 0
            headquarters_sanction_score = 0
            headquarters_embargo_score = 0

            headquarters_natural_disaster_score = 0
            headquarters_fragile_states_rate = 0
            headquarters_child_index_rate = 0
            headquarters_high_tech_export_rate = 0
            headquarters_port_time = 0
            

            global_freedom_score = 0
            peace_score = 0
            travel_advisory_score = 0
            political_stability_score = 0
            security_threats_score = 0
            corruption_score = 0
            gdp_score = 0

            economic_freedom_score = 0
            tarrif_score = 0
            sanction_score = 0
            embargo_score = 0

            natural_disaster_score = 0
            fragile_states_rate = 0
            child_index_rate = 0
            high_tech_export_rate = 0
            port_time = 0

            info = {'headquarters':[],'manufacturer':[]}
            economic_info = {'headquarters':[],'manufacturer':[]}
            production_info = {'headquarters':[],'manufacturer':[]}
            

            for country in countries:
                if country == headquarters_country:
                    headquarters_global_freedom_score = round((10-get_global_freedom_score_dict.get(country)/10),2)
                    headquarters_peace_score =  round((country_peace_score_dict.get(country)*2),2)

                    headquarters_travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)
                    
                    headquarters_economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        headquarters_tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        headquarters_tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)

                    if country == 'united states':
                        headquarters_sanction_score = 0
                    else:
                            headquarters_sanction_score = round(((get_sanction(country) / 1000) * 4),2)

                    if (country in embargo_countries) == True:
                        headquarters_embargo_score = 10
                    else:
                        headquarters_embargo_score = 0

                    headquarters_political_stability_score = 0
                    headquarters_security_threats_score = 0
                    headquarters_corruption_score = 0
                    if country == 'united states':
                        country_temp = 'usa'
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country_temp)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        headquarters_political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        headquarters_security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        headquarters_corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)


                    headquarters_gdp_score = 0 
                    if country in get_country_gdp_dict:
                        # headquarters_gdp_score = get_country_gdp_dict.get(country)
                        headquarters_gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        headquarters_gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)

                    headquarters_natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        headquarters_natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        headquarters_natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    headquarters_fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        headquarters_fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        headquarters_fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    headquarters_child_index_rate = 0
                    if country in get_child_index_dict:
                        headquarters_child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        headquarters_child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    headquarters_high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    headquarters_port_time = round((get_port_time(country) * 2),2)

                    info['headquarters'].append([country,headquarters_global_freedom_score,headquarters_peace_score,headquarters_travel_advisory_score,headquarters_political_stability_score,headquarters_security_threats_score,headquarters_corruption_score,headquarters_gdp_score])
                    economic_info['headquarters'].append([country,headquarters_economic_freedom_score,headquarters_tarrif_score,headquarters_sanction_score,headquarters_embargo_score])
                    production_info['headquarters'].append([country,headquarters_natural_disaster_score,headquarters_fragile_states_rate,headquarters_child_index_rate,headquarters_high_tech_export_rate,headquarters_port_time])
                else:
                    global_freedom_score = round(10-(get_global_freedom_score_dict.get(country)/10),2)
                    peace_score = round((country_peace_score_dict.get(country)*2),2)

                    travel_advisory_score = round((get_travel_advisories_level(country)*2.5),2)

                    economic_freedom_score = round((10 - get_economic_freedom_dict.get(country)/10),2)
                    if (country in get_tariff_rate_dict) == True:
                        tarrif_score = round(((get_tariff_rate_dict.get(country)/10) * 3), 2)
                    else:
                        tarrif_score = round(((mean(get_tariff_rate_dict.values())/10) * 3),2)
                    
                    if country == 'united states':
                        sanction_score = 0
                    else:
                        sanction_score = round(((get_sanction(country) / 1000) * 4),2)
                    
                    if (country in embargo_countries) == True:
                        embargo_score = 10
                    else:
                        embargo_score = 0

                    political_stability_score = 0
                    security_threats_score = 0
                    corruption_score = 0
                    if country.lower() == 'united states':
                        country_temp = 'usa'
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country_temp)+2.5)*2),2)
                        security_threats_score = get_security_threats_index_dict.get(country_temp)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country_temp)/10),2)
                    else:
                        political_stability_score = round((10-(get_political_stability_index_dict.get(country)+2.5)*2),2) if country in get_political_stability_index_dict else round(mean(list(get_political_stability_index_dict.values())),2)
                        security_threats_score = get_security_threats_index_dict.get(country) if country in get_security_threats_index_dict else round(mean(list(get_security_threats_index_dict.values())),2)
                        corruption_score = round((get_corruption_perceptions_index_dict.get(country)/10),2) if country in get_corruption_perceptions_index_dict else round(mean(list(get_corruption_perceptions_index_dict.values())),2)

            
                    gdp_score = 0 
                    if country in get_country_gdp_dict:
                        gdp_score = round((10-get_country_gdp_dict.get(country)/2000000000000),2)
                    else:
                        gdp_score = round(10 - mean(list(get_country_gdp_dict.values()))/2000000000000,2)


            
                    natural_disaster_score = 0
                    if country in get_natural_disaster_rate_dict:
                        natural_disaster_score = round((get_natural_disaster_rate_dict.get(country)/10),2)
                    else:
                        natural_disaster_score = round(mean(list(get_natural_disaster_rate_dict.values()))/10,2)
                        

                    fragile_states_rate = 0
                    if country in get_fragile_states_rate_dict:
                        fragile_states_rate = round((get_fragile_states_rate_dict.get(country)/12),2)
                    else:
                        fragile_states_rate = round(mean(list(get_fragile_states_rate_dict.values()))/12,2)

                    child_index_rate = 0
                    if country in get_child_index_dict:
                        child_index_rate = round((get_child_index_dict.get(country)/19.6),2)
                    else:
                        child_index_rate = round(mean(list(get_child_index_dict.values()))/19.6,2)                    

                    high_tech_export_rate = round((10 - (get_high_tech_export(country)/10)),2)
                    port_time = round((get_port_time(country) * 2),2)

                    info['manufacturer'].append([country,global_freedom_score,peace_score,travel_advisory_score,political_stability_score,security_threats_score,corruption_score,gdp_score])
                    economic_info['manufacturer'].append([country,economic_freedom_score,tarrif_score,sanction_score,embargo_score])
                    production_info['manufacturer'].append([country,natural_disaster_score,fragile_states_rate,child_index_rate,high_tech_export_rate,port_time])

            
            
            head_score_list = ([score[1:] for score in info['headquarters']]) 
            headquarters_political_risk_score = round(mean(list(itertools.chain(*head_score_list))),2)
            manu_score_list = ([score[1:] for score in info['manufacturer']]) 
            manu_political_risk_score = round(mean(list(itertools.chain(*manu_score_list))),2)
            
            total_political_risk_score = round((headquarters_political_risk_score + manu_political_risk_score)/2,2)
            
            head_score_economic_list = ([score[1:] for score in economic_info['headquarters']]) 
            headquarters_economic_risk_score = round(mean(list(itertools.chain(*head_score_economic_list))),2)
            manu__economic_score_list = ([score[1:] for score in economic_info['manufacturer']]) 
            manu_economic_risk_score = round(mean(list(itertools.chain(*manu__economic_score_list))),2)

            total_economic_risk_score = round((headquarters_economic_risk_score + manu_economic_risk_score)/2,2)


            head_score_production_list = ([score[1:] for score in production_info['headquarters']]) 
            headquarters_production_risk_score = round(mean(list(itertools.chain(*head_score_production_list))),2)
            manu__production_score_list = ([score[1:] for score in production_info['manufacturer']]) 
            manu_production_risk_score = round(mean(list(itertools.chain(*manu__production_score_list))),2)

            total_production_risk_score = round((headquarters_production_risk_score + manu_production_risk_score)/2,2)            

            political_agree_column,Security_risk_agree_column,economic_risk_agree_column,production_risk_agree_column = st.columns([1,1,1,1])
            with political_agree_column:
                political_risk_agree = st.checkbox('Get More Political Risk Info',key="1")
                if political_risk_agree:
                    get_political_risk_more_info()
            with Security_risk_agree_column:
                Security_risk_agree = st.checkbox('Get More Security Risk Info',key="2")
                if Security_risk_agree:
                    get_security_risk_more_info()
            with economic_risk_agree_column:
                economic_risk_agree = st.checkbox('Get More Economic Risk Info',key="3")    
                if economic_risk_agree:
                    get_economic_risk_more_info()
            with production_risk_agree_column:
                production_risk_agree = st.checkbox('Get More Production Risk Info',key="4")  
                if production_risk_agree:
                    get_production_risk_more_info()

            political_headquart_col, political_manufac_col,security_score = st.columns([1,2,3])
            
            with political_headquart_col:
                st.header('Political Risk')
                st.subheader('Headquarters:')

                political_risks_types = ['Country','Freedom Score','Peace Score','Travel Advisory','Political Stability','Security Threat','Corruption Index','GDP']

                headquarter_country_list = [country[0] for country in info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(headquarter_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['headquarters'],i,political_risks_types)

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(headquarters_political_risk_score),headquarters_political_risk_score)
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

                    
            with political_manufac_col:
                for i in range(5):
                    st.text('')
            
                st.subheader('Manufacturers:')
                
                manu_country_list = [country[0] for country in info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(manu_country_list)))

                for i in range(1,len(political_risks_types)):
                    risk_generator(info['manufacturer'],i,political_risks_types)
                
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_political_risk_score,2)),round(manu_political_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                


            nvd_tot_results,cve_id,scores,str_score,url_list = calculate_nvd_risk_score(ram_input)
            with security_score:
                st.header('Security Risk')
                
                st.subheader('{} CVE IDs Available'.format(nvd_tot_results))
                st.warning('Since SCRAPE restricts the amount of CVE IDs utilized owing to program performance, only 8 CVE IDs will be used in the computations. For future editions, this can be changed for more accurate results.')
                st.subheader('CVE ID:')

                cve_hyper = ''
                for i,id in enumerate(cve_id):
                    if(i == 0):
                        cve_hyper = '[{}]({})'.format(id,url_list[i])
                    else:
                        cve_hyper += ', [{}]({})'.format(id,url_list[i])
                        
                st.write(cve_hyper)
                colored_cve_scores = ''
                for i,score in enumerate(scores):
                    if(i == 0):
                        colored_cve_scores = '<span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)
                    else:
                        colored_cve_scores += ', <span style="color:{}; font-size: 20px;">{}</span>'.format(color_picker(score),score)       
                st.subheader('Scores: ')
                st.markdown('**{}**'.format(colored_cve_scores), unsafe_allow_html=True)
            cve_tot_score = round(mean(scores),2)
            st.text('')


            economic_headquartes_risk_score,economic_manufac_risk_score,production_headquarters_risk_score,production_manufac_risk_score = st.columns([1,2,1,2])
            
            with economic_headquartes_risk_score:

                st.header('Economic Risk')

                st.subheader('Headquarters:')

                economic_headquarter_country_list = [country[0] for country in economic_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(economic_headquarter_country_list)))

                
                economic_risks_types = ['Country','Economic Freedom Score','Tarrif Score','Sanction Score','Embargo Score']
                
                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['headquarters'],i,economic_risks_types)  


                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_economic_risk_score,2)),round(headquarters_economic_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with economic_manufac_risk_score:
                for i in range(5):
                    st.text('')
                
                st.subheader('Manufacturers:')
                econonic_manu_country_list = [country[0] for country in economic_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(', '.join(econonic_manu_country_list)))

                for i in range(1,len(economic_risks_types)):
                    risk_generator(economic_info['manufacturer'],i,economic_risks_types)  

                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_economic_risk_score,2)),round(manu_economic_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 
                

            with production_headquarters_risk_score:

                st.header('Production Risk')
                st.subheader('Headquarters:')
                
                production_risks_types = ['Country','Natural Disaster Score','Fragile State Score','Children In Employment Score','Product Export Score','Port Time Score']
                production_headquarter_country_list = [country[0] for country in production_info['headquarters']]
                st.markdown('Country: **{}**'.format(' '.join(production_headquarter_country_list)))
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['headquarters'],i,production_risks_types)  

                head_text = '<span style="font-size: 20px;">Headquarters Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(headquarters_production_risk_score,2)),round(headquarters_production_risk_score,2))
                st.markdown('**{}{}**'.format(head_text,colored_head_tot_scores),unsafe_allow_html=True) 

        
            with production_manufac_risk_score:
                for i in range(5):
                    st.text('')

                st.subheader('Manufacturers:')                

                production_manufac_country_list = [country[0] for country in production_info['manufacturer']]
                st.markdown('Country: **_{}_**'.format(' '.join(production_manufac_country_list)))
                # ***** FIX CAPITALIZE LATER ********** 
                for i in range(1,len(production_risks_types)):
                    risk_generator(production_info['manufacturer'],i,production_risks_types)    
        
                manu_text = '<span style="font-size: 20px;">Manufacturer Risk Score:</span>'  
                colored_head_tot_scores = '<span style="color:{}; font-size: 35px;">  {}</span>'.format(color_picker(round(manu_production_risk_score,2)),round(manu_production_risk_score,2))
                st.markdown('**{}{}**'.format(manu_text,colored_head_tot_scores),unsafe_allow_html=True) 


    ########## Total column calculation #########################

        for i in range(4):
            st.text('')
        c1,c2 = st.columns([1,1.35])
        with c2:
            st.title('Total Risks')
        colT5,colT1,colT2, colT3,colT4,colT6 = st.columns([3,1,1,1,1,3])


        with colT1:
            tot_metric_picker('Political Risk Score',total_political_risk_score)
        with colT2:
            tot_metric_picker('Security Risk Score',cve_tot_score)
        with colT3:
            tot_metric_picker('Economic Risk Score',total_economic_risk_score)
        with colT4:
            tot_metric_picker('Production Risk Score',total_production_risk_score)


            

        bar_graph,a,b = st.columns([0.7,2,1])
        with a:
            for i in range(2):
                st.text('')    
                
            data = {'Political':total_political_risk_score, 'Security':cve_tot_score, 'Economic': total_economic_risk_score, 'Production':total_production_risk_score}
            risk_type = list(data.keys())
            values = list(data.values())
            colors = ["red" if i >= 7.0 else "green" if i < 4.0 else 'orange' for i in values]
            fig = plt.figure(figsize = (8, 4))
            leg_colors = {'High':'red', 'Medium':'orange','Low':'green'}         
            labels = list(leg_colors.keys())
            handles = [plt.Rectangle((0,0),1,1, color=leg_colors[label]) for label in labels]
            plt.legend(handles,labels)

            plt.bar(risk_type, values,color=colors)
            plt.xlabel("Risk Type",fontsize=10)
            plt.ylabel("Risk Score",fontsize=10)
            plt.rcParams.update({'font.size': 6})
            st.pyplot(fig)

        
        for i in range(3):
            st.text('')
            
        st.markdown('### **{}** Headquarters Location: **_{}_**'.format(company_name.capitalize(),headquarters_location))
         
        head_latitude, head_longitude = get_lat_long(headquarters_location)       
        set_map(head_latitude,head_longitude)



# Test Example inputs
# NVIDIA GeForce RTX 3060, AMD Radeon RX 6600 XT
# Intel Atom 230 @ 1.60GHz
# samsung 18asf1g72pdz-2g1b1 16gb
# antec earthwatts green series
# Acer SSD FA100 512GB




