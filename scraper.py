from bs4 import BeautifulSoup
import requests
import datetime
import scraperwiki
import time

requests.packages.urllib3.disable_warnings()

cities = {
    'Edinburgh': 'gcvwr3zrw',
    'London': 'gcpvj0v07',
    'Tirana': 'srq545gke',
    'Andorra la Vella': 'sp91f3j53',
    'Vienna': 'u2edhqw16',
    'Minsk': 'u9edes5nk',
    'Brussels': 'u1514zps6',
    'Sarajevo': 'srv1e3wwp',
    'Sofia': 'sx8dg57xm',
    'Zagreb': 'u25kdgqqt',
    'Nicosia': 'swr8p3cne',
    'Prague': 'u2fkbqee7',
    'Copenhagen': 'u3buvefsh',
    'Tallinn': 'ud9d5qt9m',
    'Helsinki': 'ud9wx0fhw',
    'Paris': 'u09tvnxyj',
    'Berlin': 'u33dc23vw',
    'Gibraltar': 'eykjqrrw2',
    'Athens': 'swbb6wgcq',
    'St. Peter Port': 'gby1q7guf',
    'Budapest': 'u2mw1xp5d',
    'Reykjavik': 'ge2kughet',
    'Dublin': 'gc7x92466',
    'Douglas': 'gcsu1fnc5',
    'Rome': 'sr2y7gxtj',
    'Saint Helier': 'gbwxb0rjg',
    'Pristina': 'srx49k0yq',
    'Riga': 'ud1h5dkz4',
    'Vaduz': 'u0qu0eu20',
    'Vilnius': 'u99zpk026',
    'Luxembourg': 'u0u65rpxp',
    'Skopje': 'srrqeyx4w',
    'Valletta': 'sq6k4r011',
    'Chisinau': 'u8ke89d1e',
    'Monaco': 'spv2bfe5f',
    'Podgorica': 'srt9qspk8',
    'Amsterdam': 'u173zeb54',
    'Oslo': 'u4xsvmcv8',
    'Warsaw': 'u3qcnzbf7',
    'Lisbon': 'eycs2h2ky',
    'Bucharest': 'sxfsf0hxx',
    'Moscow': 'ucftnugpr',
    'Belgrade': 'srywcexdg',
    'Bratislava': 'u2s4p9jgu',
    'Ljubljana': 'u24qcn17n',
    'Madrid': 'ezjmun1p8',
    'Stockholm': 'u6scdbwyk',
    'Bern': 'u0m6ftt2f'
}

URL = 'https://www.metoffice.gov.uk/weather/forecast/'

table_entries = []

for city_name, city_code in cities.items():
    # Wait for 1 second (good practice)
    time.sleep(1)

    response = requests.get(URL + city_code, verify=False,timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table_entry = {
        'date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'city': city_name
    }

#     print(city_name)
    for day_n in range(0,7):
        day_id = 'tabDay' + str(day_n)
        day = soup.find(id=day_id)
        max_temp = day.find("span", class_="tab-temp-high")['data-value']
        min_temp = day.find("span", class_="tab-temp-low")['data-value']
        
#         print('Day: ' + str(day_n))
#         print('Max Temperature: ' + max_temp)
#         print('Min Temperature: ' + min_temp)
        
        table_entry['day'+str(day_n)+'_maxtemp'] = max_temp
        table_entry['day'+str(day_n)+'_mintemp'] = min_temp
        
    table_entries.append(table_entry)
    
for table_entry in table_entries:
    scraperwiki.sql.save(unique_keys=['date','city'], data=table_entry)
