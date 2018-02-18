from PyPDF2 import PdfFileMerger, utils
from pandas import date_range
from bs4 import BeautifulSoup
from subprocess import Popen
from io import BytesIO
from tqdm import tqdm
import requests
import pycurl


class writer():
    def __init__(self):
        self.merger = PdfFileMerger()
        self.local_files = []

    def append(self, doc):
        try:
            self.merger.append(doc)
        except utils.PdfReadError:
            raise Exception('Error')

    def append_local(self, fn):
        self.local_files.append(fn)

        with open(fn, 'rb') as f:
            self.merger.append(f)

    def write(self, date):
        self.merger.write(str(date).split(' ')[0]+'.pdf')

    def remove_local(self):
        [Popen(['rm', file]) for file in self.local_files]
        self.local_files = []


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
        r = requests.get(self.url, page)
        
        with open(fn, 'wb') as f:
            f.write(r.content)
        
        return fn


    def get_pages(self):
        url = 'http://hemeroteca.abc.es/nav/Navigate.exe/hemeroteca/madrid/abc/{}/{}/{}/001.html'.format(
            self.year, self.month, self.day
        )

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        self.pages = int((s.find_all('li', class_='current')[1].text[6:]).split('/')[1])

    def get_url(self, page):
        url = 'http://hemeroteca.abc.es/nav/Navigate.exe/hemeroteca/madrid/abc/{}/{}/{}/{}.html'.format(
            self.year, self.month, self.day, page
        )

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        self.url = 'http://hemeroteca.abc.es'+(s.find('li', class_='download').a['href'])
        print self.url

for date in date_range('13-08-1935', '14-08-1935'):
    wr = writer()
    np = newspaper(date)

    for page in tqdm(range(1, np.pages+1)):
        doc = np.buff_pdf(page)
       
        try:
            wr.append(doc)
        except Exception:
            fn = np.save_pdf(page)
            wr.append_local(fn)
        
    wr.write(date)
    wr.remove_local()
