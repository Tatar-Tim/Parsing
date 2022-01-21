from bs4 import BeautifulSoup
from requests import get
import itertools
import pandas as pd
import time
import random
import numpy as np


def read_file():
    "Функция для чтения вводных данных через файл эксель"
    text = pd.read_excel('Тестовая выборка.xlsx', engine='openpyxl')
    house = []
    regions = []
    Adress_Region = (text['Adress_Region'])   
    Adress_City = (text['Adress_City'])
    Adress_Street = (text['Adress_Street'])
    Adress_House = (text['Adress_House'])
    Adress_Block = (text['Adress_Block'])
    Adress_TypeCity = (text['Adress_TypeCity'])
    #Замена пустых значения на символ ''
    Adress_Region = Adress_Region.replace(np.nan,'')
    Adress_City = Adress_City.replace(np.nan,'')
    Adress_Street = Adress_Street.replace(np.nan,'')
    Adress_House = Adress_House.replace(np.nan,'')
    Adress_Block = Adress_Block.replace(np.nan,'')
    Adress_TypeCity = Adress_TypeCity.replace(np.nan,'')

    for i in range (len(Adress_Street)):
        if Adress_Street[i] == '':
            continue
        else:
            inf =  f'{Adress_Region[i]} {Adress_TypeCity[i]} {Adress_City[i]} {Adress_Street[i]} {Adress_House[i]} {Adress_Block[i]}'
            regions.append(Adress_Region[i])
            house.append (inf)
    return house, regions

# данные, которые нужно получить
title = []
url = []
operation_year = []
floors_number = []
series_type = []
type_house = []
accident_rate = []
cadastral_number = []
floor_type = []
wall_material = []
unknown_house = []
regions = []
house, region = read_file()
#Основной цикл парсинга:
#1ый цикл это чтение одной строки дома, которой надо найти
#2ой цикл это получение ссылок с поиска
#3ий цикл это открытие страницы и основной парсинг дома
for i in range (5):
    url = []
    sapo_url = 'https://www.reformagkh.ru/search/houses?query='
    sapo_url += house[i] 
    r = get(sapo_url)
    page_html = BeautifulSoup(r.text, 'html.parser')
    house_containers = page_html.find_all('a', class_="text-dark")
    if house_containers == []:
        unknown_house.append(house[i])
    else:
        regions.append(region[i])
    for container in house_containers:
    #ссылка на другой дом, ссылок может быть несколько, там могут вылезти, например, иногда вылезает даже другой город
    #поэтому в дальнейшем будет использоваться только первый дом, появившийся в поисковике
        sait_url =container.get('href')
        url.append(sait_url)
    #из-за особенностей, того, что некоторые строки с описанием дома могут осутствовать или некоторые данные могут быть не заполнены
    #используется обработка данных через try, except        
    for j in range (1):
      time.sleep(random.randint(0,10))
      sapo_url = 'https://www.reformagkh.ru'
      house1 = sapo_url
      if url == []:
          continue
      else:
          house1 +=url[j]
      r = get(house1)
      page_html = BeautifulSoup(r.text, 'html.parser')
      house_passport = page_html.find('div', class_="container d-flex justify-content-center").find('a', class_= "tab-title text-uppercase f-14 lh-22 fw-600 text-black text-align-center").get('href')
      house1 = sapo_url
      house1 +=house_passport
      r = get(house1)
      page_html = BeautifulSoup(r.text, 'html.parser')
      year = page_html.find('td', string = 'Год постройки')
      if year != None:
        year = page_html.find('td', string = 'Год постройки').next_sibling.next_sibling.string  
      else: 
        try: 
            year = page_html.find('td', string = 'Год ввода дома в эксплуатацию').next_sibling.next_sibling.string
            year = year.strip()
        except AttributeError:
            year = 'Не заполнено'
    
      name = page_html.find('td', string = 'Адрес дома')
      if name != None:
        name = page_html.find('td', string = 'Адрес дома').next_sibling.next_sibling.string
        name = name.strip()
        
      type_home = page_html.find('td', string = 'Тип дома')
      if type_home !=None:
        type_home = page_html.find('td', string = 'Тип дома').next_sibling.next_sibling.string
      try: 
        type_home = page_html.find('td', string = 'Тип дома').next_sibling.next_sibling.next_sibling.next_sibling.string
      except AttributeError: 
        type_home = page_html.find('td', string = 'Тип дома').next_sibling.next_sibling.string
      
      type_home = type_home.strip() 
    
      seria_home = page_html.find('td', string = 'Серия, тип постройки здания')
      if seria_home !=None:
        seria_home = page_html.find('td', string = 'Серия, тип постройки здания').next_sibling.next_sibling.string
        seria_home = seria_home.strip() 

      floors = page_html.find('td', string = 'Количество этажей, ед.')
      if floors != None:
        floors = page_html.find('td', string = 'Количество этажей, ед.').next_sibling.next_sibling.string
        floors = floors.strip()

      cadastr = page_html.find('td', string = 'Кадастровый номер земельного участка')
      if cadastr != None:
        cadastr = page_html.find('td', string = 'Кадастровый номер земельного участка').next_sibling.next_sibling.string
        cadastr = cadastr.strip()
      
      type_floor = page_html.find('td', string = 'Стены и перекрытия. Тип перекрытий')
      if type_floor !=None:
          try:
            type_floor = page_html.find('td', string = 'Стены и перекрытия. Тип перекрытий').next_sibling.next_sibling.next_sibling.next_sibling.string
            type_floor = type_floor.strip()
          except AttributeError:
             type_floor = page_html.find('td', string = 'Стены и перекрытия. Тип перекрытий').next_sibling.next_sibling.string   
             type_floor = type_floor.strip()

      material = page_html.find('td', string = 'Стены и перекрытия. Материал несущих стен')
      if material !=None:
            try:
              material = page_html.find('td', string = 'Стены и перекрытия. Материал несущих стен').next_sibling.next_sibling.next_sibling.next_sibling.string
              material= material.strip()
            except AttributeError:
              material = page_html.find('td', string = 'Стены и перекрытия. Материал несущих стен').next_sibling.next_sibling.string
              material= material.strip()

      accident = page_html.find('td', string = 'Факт признания дома аварийным')
      if accident == None:
        accident = 'Нет'
 
      title.append(name), operation_year.append(year), type_house.append(type_home), series_type.append(seria_home), floors_number.append(floors)
      cadastral_number.append(cadastr), floor_type.append(type_floor),wall_material.append(material), accident_rate.append(accident)

cols = ['регион', 'дом', 'год', 'этажи', 'серия', 'тип', 'аварийность', 'кадастр',
        'тип_перекрытий', 'материал']

lisboa = pd.DataFrame({'дом':title, 'регион':regions,  'год':operation_year, 'этажи':floors_number, 'серия':series_type,
                       'тип':type_house, 'аварийность':accident_rate, 'кадастр':cadastral_number,
                       'тип_перекрытий':floor_type, 'материал':wall_material})[cols]

#определить количество объектов для Материал несущих стен = Кирпичный по каждому региону.
material = lisboa.query("материал == 'Кирпич'")
material.value_counts('регион')
print(material)
#определить максимальное количество этажей для каждого Материал несущих стен в каждом городе. 

max = lisboa[['регион', 'материал', 'этажи']]
max = max.sort_values(by = ['регион', 'материал'])
max = max.groupby(['регион','материал', 'этажи']).max()
print(max)