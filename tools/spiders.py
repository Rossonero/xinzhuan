# -*- coding: utf-8 -*-

import os
import sys
import requests
import bs4
import re
import datetime
from urlparse import urljoin
from subprocess import Popen, PIPE

sys.path.append('/home/perchouli/workspaces/xinzhuan')

from media.models import Medium, Unit
from journalists.models import Journalist
from articles.models import Article

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

    def nfzm(self, page=0):
        list_2012 = [{"url":"http://www.infzm.com/enews/infzm/3168","date":"2012-12-27"},
            {"url":"http://www.infzm.com/enews/infzm/3146","date":"2012-12-20"},
            {"url":"http://www.infzm.com/enews/infzm/3129","date":"2012-12-13"},
            {"url":"http://www.infzm.com/enews/infzm/3121","date":"2012-12-06"},
            {"url":"http://www.infzm.com/enews/infzm/3109","date":"2012-11-29"},
            {"url":"http://www.infzm.com/enews/infzm/3083","date":"2012-11-22"},
            {"url":"http://www.infzm.com/enews/infzm/3072","date":"2012-11-15"},
            {"url":"http://www.infzm.com/enews/infzm/3060","date":"2012-11-09"},
            {"url":"http://www.infzm.com/enews/infzm/3043","date":"2012-11-01"},
            {"url":"http://www.infzm.com/enews/infzm/3027","date":"2012-10-25"},
            {"url":"http://www.infzm.com/enews/infzm/3019","date":"2012-10-18"},
            {"url":"http://www.infzm.com/enews/infzm/3012","date":"2012-10-11"},
            {"url":"http://www.infzm.com/enews/infzm/3005","date":"2012-10-04"},
            {"url":"http://www.infzm.com/enews/infzm/2997","date":"2012-09-27"},
            {"url":"http://www.infzm.com/enews/infzm/2988","date":"2012-09-20"},
            {"url":"http://www.infzm.com/enews/infzm/2973","date":"2012-09-13"},
            {"url":"http://www.infzm.com/enews/infzm/2963","date":"2012-09-06"},
            {"url":"http://www.infzm.com/enews/infzm/2954","date":"2012-08-30"},
            {"url":"http://www.infzm.com/enews/infzm/2943","date":"2012-08-24"},
            {"url":"http://www.infzm.com/enews/infzm/2934","date":"2012-08-17"},
            {"url":"http://www.infzm.com/enews/infzm/2921","date":"2012-08-09"},
            {"url":"http://www.infzm.com/enews/infzm/2910","date":"2012-08-02"},
            {"url":"http://www.infzm.com/enews/infzm/2895","date":"2012-07-26"},
            {"url":"http://www.infzm.com/enews/infzm/2852","date":"2012-07-19"},
            {"url":"http://www.infzm.com/enews/infzm/2841","date":"2012-07-12"},
            {"url":"http://www.infzm.com/enews/infzm/2832","date":"2012-07-05"},
            {"url":"http://www.infzm.com/enews/infzm/2818","date":"2012-06-28"},
            {"url":"http://www.infzm.com/enews/infzm/2784","date":"2012-06-21"},
            {"url":"http://www.infzm.com/enews/infzm/2772","date":"2012-06-14"},
            {"url":"http://www.infzm.com/enews/infzm/2759","date":"2012-06-07"},
            {"url":"http://www.infzm.com/enews/infzm/2748","date":"2012-05-31"},
            {"url":"http://www.infzm.com/enews/infzm/2741","date":"2012-05-24"},
            {"url":"http://www.infzm.com/enews/infzm/2715","date":"2012-05-17"},
            {"url":"http://www.infzm.com/enews/infzm/2698","date":"2012-05-10"},
            {"url":"http://www.infzm.com/enews/infzm/2682","date":"2012-05-03"},
            {"url":"http://www.infzm.com/enews/infzm/2673","date":"2012-04-26"},
            {"url":"http://www.infzm.com/enews/infzm/2658","date":"2012-04-19"},
            {"url":"http://www.infzm.com/enews/infzm/2650","date":"2012-04-12"},
            {"url":"http://www.infzm.com/enews/infzm/2642","date":"2012-04-05"},
            {"url":"http://www.infzm.com/enews/infzm/2636","date":"2012-03-29"},
            {"url":"http://www.infzm.com/enews/infzm/2628","date":"2012-03-22"},
            {"url":"http://www.infzm.com/enews/infzm/2596","date":"2012-03-15"},
            {"url":"http://www.infzm.com/enews/infzm/2539","date":"2012-03-08"},
            {"url":"http://www.infzm.com/enews/infzm/2524","date":"2012-03-01"},
            {"url":"http://www.infzm.com/enews/infzm/2508","date":"2012-02-23"},
            {"url":"http://www.infzm.com/enews/infzm/2500","date":"2012-02-16"},
            {"url":"http://www.infzm.com/enews/infzm/2492","date":"2012-02-09"},
            {"url":"http://www.infzm.com/enews/infzm/2471","date":"2012-02-02"},
            {"url":"http://www.infzm.com/enews/infzm/2458","date":"2012-01-26"},
            {"url":"http://www.infzm.com/enews/infzm/2444","date":"2012-01-12"},
            {"url":"http://www.infzm.com/enews/infzm/2438","date":"2012-01-05"}]

        
        for e in list_2012[::-1]:
            url =  e['url']
            print url
            date = e['date']
            r = requests.get(url, cookies={'PHPSESSID': 'l19dgbf6ticijmo9ka9osvufk0'})
            content = bs4.BeautifulSoup(r.content).find('div', {'id' : 'enews_index'})
            issue = content.find('div', {'class' : 'cover'}).find_all('p')[-1]
            p = re.compile('(\d+)-(\d+)-(\d+)')
            issue = int(p.search(issue.text).group())

            #Get topnews
            # topnews = content.find('dl', {'class' : 'topnews'})
            # if topnews:
            #     topnews_url = topnews.find('a').get('href')
            #     article = self._get_nfzm_article(topnews_url, date, issue)
            #     article.page = u'头版'
            #     if not Article.objects.filter(url=topnews_url).count():
            #         article.save()

            page_list = content.find('div', {'class' : 'side-2'}).find('h2')
            for page in page_list:
                article_urls = page.next.next.find_all('a')
                for article_url in article_urls:
                    print 'Article' + article_url.get('href')
                    article = self._get_nfzm_article(article_url.get('href'), date, issue)
                    article.page = page.next
                    if not Article.objects.filter(url=article_url.get('href')).count():
                        article.save()


    def zgqnb(self):
        start_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        for i in range(366):
            publication_date = start_date + datetime.timedelta(days=i)
            url = 'http://zqb.cyol.com/html/%s/nbs.D110000zgqnb_01.htm' % (datetime.datetime.strftime(publication_date, '%Y-%m/%d'))
    
    def cnki(self):
        domain = 'http://epub.cnki.net'
        for page in range(41, 81):
            # url = r'http://epub.cnki.net/kns/Navi/Newbrief.aspx?curpage='+ str(page) +'&pagename=ASP.navi_newitem_aspx&dbPrefix=25_Catalog&dbCatalog=%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93&ConfigFile=25_Catalog.xml&NaviID=25&t=1357870014588&DisplayMode=listmode'

            # url = r'http://acad.cnki.net/Kns55/Navi/Newbrief.aspx?pagename=ASP.navi_newitem_aspx&dbPrefix=25_Catalog&dbCatalog=%E4%B8%AD%E5%9B%BD%E9%87%8D%E8%A6%81%E6%8A%A5%E7%BA%B8%E5%85%A8%E6%96%87%E6%95%B0%E6%8D%AE%E5%BA%93&ConfigFile=25_Catalog.xml&NaviID=25&t=1357892388302'
            url = 'http://epub.cnki.net/kns/Navi/Newbrief.aspx?curpage='+str(page)+'&RecordsPerPage=20&QueryID=14&ID=&turnpage=1&tpagemode=L&dbPrefix=25_CATALOG&Fields=Value%3dValue%3dValue%3dValue%3dValue=&DisplayMode=listmode&pagename=ASP.navi_newitem_aspx&NaviID=25&sKuaKuID=14'
            cookies = {
                'SID_sug' : '111056',
                'SID_kcms' : '202111',
                'ASP.NET_SessionId' : 'qkariv45hxzawr551dx0va45',
                'SID' : '120104',
                # 'ASPSESSIONIDSAACSBRS' : 'LLDPLAPAJJLMOFAPIIMCAEGG',
                'pgv_pvi' : '1464069120',
                'pgv_si' : 's4107717632',
                'LID' : 'WEEvREcwSlJHSldTTEYyQXpVbCt3RkR0T1VsdmlYWllJWEFxZWExU3lJS0xyZm12ZEE0Y2NPMDJ1QkdZZWJRPQ==',
            }
            response = bs4.BeautifulSoup(requests.get(url, cookies=cookies).content)
            content = response.find('table', {'class' : 'GridTableContent'})
            # print content
            for a in content.find_all('a'):
                if a.get('href').find('download.aspx') != -1 : continue
                article_link          = a.get('href')
                article_link_response = requests.get(domain + article_link, cookies=cookies)
                article_soup          = bs4.BeautifulSoup(article_link_response.content)
                article_content       = article_soup.find('div', {'id' : 'content'})

                article               = self._get_rmrb_article(article_content)
                # article.url           = article_link_response.url



                link = article_content.find('li', {'class' : 'pdf'})
                if not link:
                    link = article_content.find('li', {'class' : 'pdfD'})

                file_link = link.find('a').get('href')
                file_r_link = file_link.replace('\n', '').replace(' ','')
                file_download_link = urljoin(article_link_response.url, file_r_link)
                print file_download_link
                r = requests.get(file_download_link, cookies=cookies, stream=True)
                with open('article.pdf', 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                try:
                    p1 = Popen(['pdftotext', '-layout', '-nopgbrk', 'article.pdf'], stdout=PIPE)
                    p1.communicate()
                    f = open('article.txt', 'rw')
                except:
                    continue
                article_content = f.read()
                print article_content
                f.close()
                Popen(['rm', 'article.pdf'], stdout=PIPE)
                article.content = article_content
                article.save()
                # break
            # break

    def _get_nfzm_article(self, url, date, issue):
        medium = Medium.objects.get(pk=951)
        article                  = Article()
        article.medium           = medium
        article.issue            = issue
        article.url              = url
        article.publication_date = date

        r = requests.get(url, cookies={'PHPSESSID': 'l19dgbf6ticijmo9ka9osvufk0'})
        content = bs4.BeautifulSoup(r.content)
        article.title = content.title.string.split('-')[-1].strip()
        article.content = content.find('section', {'id' : 'articleContent'}).text

        author = content.find('span', {'class' : 'author'}).find_all('em')
        if author[1].text.find(u'南方周末记者') != -1:
            author, created = Journalist.objects.get_or_create(medium=medium, name=author[2].text.strip())
            if not created:
                article.author = author
        elif author[1].text.find(u'南方周末特约撰稿') != -1:
            article.author_name = author[2].text.strip()
        elif author[1].text.find(u'南方周末编辑部') != -1:
            article.author_name = u'南方周末编辑部'

        print article.author or article.author_name
        return article


    def _get_rmrb_article(self, content):
        medium = Medium.objects.get(pk=1081)
        article = Article()
        article.medium = medium
        article.title = content.find('h1').text.strip()

        for author_name in content.find_all('div', {'class' : 'summary'})[0].find_all('a'):
            try:
                author = Journalist.objects.get(medium=medium, name=author_name.text.strip())
            except:
                pass
            else:
                article.author = author
                break

        for li in content.find_all('div', {'class' : 'summary'})[-1].find_all('li'):
            if li.text.find(u'报纸日期') != -1:
                p = re.compile('(\d+)-(\d+)-(\d+)')
                publication_date = p.search(li.text).group()

            if li.text.find(u'版名') != -1:
                page = li.text.replace('\n','').replace(u'【版名】', '').replace(' ', '')
            else:
                page = '头版'

        article.issue = self._get_issue_from_date(publication_date, 'rmrb')
        article.page = page
        article.publication_date = publication_date
        article, created = Article.objects.get_or_create(medium=article.medium, title=article.title)
        print article.title
        return article

    def _get_unit(self, unit_name):
        print unit_name
        unit, created = Unit.objects.get_or_create(name=unit_name)

        return unit

    def _get_publication(self, data):
        newspaper, created = Medium.objects.get_or_create(**data)

        return newspaper

    def _get_issue_from_date(self, date, medium):
        ISSUE = {
            'rmrb' : 23185
        }
        start_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        publication_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return ISSUE[medium] + (publication_date - start_date).days


if __name__ == '__main__':
    s = Spiders()
    s.cnki()