# -*- coding: utf-8 -*-

import os
import sys
import requests
import bs4

sys.path.append('/home/perchouli/workspaces/xinzhuan')

from media.models import Medium, Unit
from journalists.models import Journalist

class Spiders():

    def gapp(self, page=0):
        url_base = 'http://press.gapp.gov.cn:8088'
        data = {}
        data['t4']                                     = 3
        data['mediaName']                              = ''
        data['PeriodicalId']                           = ''
        data['mypretime']                              = 0
        data['test']                                   = 1
        data['mediaSelect']                            = 0
        data['requestPaginationModel.pagination.page'] = page

        cookies = {'JSESSIONID': 'DEC84BB2CFA15D6E9F3727AE1D2E03E6.tomcat1'}
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r = requests.post('http://press.gapp.gov.cn:8088/press_search/pages/query/queryAction!findGappMediaPaging.action', data=data, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(r.content)
        data_table = soup.find('table', attrs={'class': 'data_table'})

        rows = data_table.find_all('tr')
        for row in rows[1:len(rows)-1]:
            print row
            row_td = row.find_all('td')
            urls = row.find_all('td')[-1].find_all('a')
            journalist_list_url = url_base + urls[0].get('href')
            newspaper_detail_url = url_base + urls[1].get('href')
            
            # newspaper_detail = bs4.BeautifulSoup(requests.get(newspaper_detail_url).content)

            # competent_dept = self._get_unit(
            #         newspaper_detail.find_all('td')[11].text.replace('\t','').replace('\n','').replace('\ ','')
            #     )

            # sponsor = self._get_unit(
            #     newspaper_detail.find_all('td')[13].text.replace('\t','').replace('\n','').replace('\ ','')
            # )
            # language = newspaper_detail.find_all('td')[15].text.replace('\t','').replace('\n','')
            # if language.find(u'汉语') != -1:
            #     language = 'zh'
            # elif language.find(u'英语') != -1:
            #     language = 'en'
            # elif language.find(u'锡伯语') != -1:
            #     language = 'sjo'
            # elif language.find(u'壮语') != -1:
            #     language = 'za'
            # elif language.find(u'俄语') != -1:
            #     language = 'ru'
            # elif language.find(u'朝鲜语') != -1:
            #     language = 'ko'
            # elif language.find(u'蒙语') != -1:
            #     language = 'mn'
            # elif language.find(u'藏语') != -1:
            #     language = 'bo'
            # elif language.find(u'维吾尔语') != -1:
            #     language = 'ug'
            # elif language.find(u'哈萨克语') != -1:
            #     language = 'kk'
            # else:
            #     language = 'zh'
            data = {
                'name' : row_td[0].text,
                'address' : row_td[1].text,
                # 'language' : language,
                #'cn' : row_td[2].text.replace('\t','').replace('\n',''),
                'code' : row_td[2].text.replace('\t','').replace('\n',''),
                'phone' : row_td[4].text.replace('\t','').replace('\n',''),
                # 'sponsor' : sponsor,
                # 'competent_dept' : competent_dept,
                'category' : 'radio_and_tv',
            }
            newspaper = self._get_publication(data)

            newspaper_journalists = bs4.BeautifulSoup(requests.get(journalist_list_url).content).find('table', attrs={'class':'data_table'}).find_all('td')
            for j in newspaper_journalists:
                name = j.text.replace(' ','').replace('\t','')
                if len(name) <= 1: continue

                try:
                    journalist = Journalist.objects.get(name=name, medium=newspaper)
                except:
                    Journalist.objects.create(name=name, medium=newspaper)


    def cmss(self):
        pass

    def _get_unit(self, unit_name):
        print unit_name
        unit, created = Unit.objects.get_or_create(name=unit_name)

        return unit

    def _get_publication(self, data):
        newspaper, created = Medium.objects.get_or_create(**data)

        return newspaper

    def _add_journalist(self):
        pass

if __name__ == '__main__':
    s = Spiders()
    for i in range(5, 268):
        print i
        s.gapp(i)
