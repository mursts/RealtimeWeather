#!/usr/bin/env python
# coding: utf-8

import re
import requests
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from mongoengine import connect
from model.weather import Weather

URL = 'http://weather-station.step.aichi-edu.ac.jp/'
POINTS = [u'名古屋', u'岡崎']

def main():
    r = requests.get(URL)
    if r.status_code != requests.codes.ok:
        raise Exception(u'ソースの取得失敗.')
    content = r.content

    bs = BeautifulSoup(content)
    
    point_matcher = re.compile(u'.*(' + '|'.join(POINTS) + ').*')

    connect('realtimeweather')

    for point_data in bs.findAll('div', {'class': 'aData'})[1:]:
        model = Weather()

        point_name = point_data.find('p', {'class': 'chiten_name'}).text
        m = point_matcher.search(point_name)
        if not m:
            continue

        model.point = m.group(1)
        data_list = point_data.findAll('td', {'class': 'td_data'})
        model.temperature = float(data_list[0].text.replace(u'℃', u''))
        model.humidity = float(data_list[1].text.replace(u'％', u''))
        model.pressure = float(data_list[2].text.replace(u'hPa', ''))
        model.wind_direction = data_list[3].text
        model.wind_speed = float(data_list[4].text.replace(u'm/s', u''))
        model.rainfall = float(data_list[5].text.replace(u'mm/h', ''))

        date = point_data.find('table').find('tr').findAll('td')[1].text
        model.date = datetime.strptime(date, '%Y/%m/%d %H:%M')

        model.save()

if __name__ == '__main__':
    main()
