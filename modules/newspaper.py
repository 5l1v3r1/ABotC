#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from io import BytesIO
import requests
import pycurl


class newspaper():
    def __init__(self, date):
        self.year = str(date.year)
        self.month = str(date.month) if date.month >= 10 else '0'+str(date.month)
        self.day = str(date.day) if date.day >= 10 else '0'+str(date.day)
        self.get_pages()

    def buff_pdf(self, page):
        page = '0'+str(page) if page >= 10 else '00'+str(page)
        self.get_url(page)

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
            
        return buffer

    def save_pdf(self, page):
        page = '0'+str(page) if page >= 10 else '00'+str(page)
        fn = self.day+'-'+self.month+'-'+self.year+'-'+str(page)+'.pdf'
        r = requests.get(self.url)
        
        with open(fn, 'wb') as f:
            f.write(r.content)
        
        return fn


    def get_pages(self):
        url = 'http://hemeroteca.abc.es/nav/Navigate.exe/hemeroteca/madrid/abc/{}/{}/{}/001.html'.format(
            self.year, self.month, self.day)

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        self.pages = int((s.find_all('li', class_='current')[1].text[6:]).split('/')[1])

    def get_url(self, page):
        url = 'http://hemeroteca.abc.es/nav/Navigate.exe/hemeroteca/madrid/abc/{}/{}/{}/{}.html'.format(
            self.year, self.month, self.day, page)

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        self.url = 'http://hemeroteca.abc.es'+(s.find('li', class_='download').a['href'])


if __name__ == '__main__':
    exit()