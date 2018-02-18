from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from pandas import date_range
from bs4 import BeautifulSoup
from tqdm import tqdm
from io import BytesIO
import pycurl
import time

writer = PdfFileWriter()
dates = date_range('01-01-1931', '31-12-1939')

def pages(buffer):
    s = BeautifulSoup(buffer.getvalue(), 'html.parser')
    return int(s.find_all('li', class_='current')[1].text[7:10])

def download(num, he=True):
    time.sleep(1.5)
    if he:
        url = 'http://hemeroteca.abc.es/cgi-bin/pagina.pdf?fn=exec;command=stamp;path=H:\cran\data\prensa_pages\Madrid\ABC\1932\193201\19320126\32E26-'+num+'.xml;id=0000261090'
    else:
        year = str(num.year)
        month = str(num.month) if num.month >= 10 else str(0)+str(num.month)
        day = str(num.day) if num.day >= 10 else str(0)+str(num.day)

        url = 'http://hemeroteca.abc.es/cgi-bin/pagina.pdf?fn=exec;command=stamp;path=H:\cran\data\prensa_pages\Madrid\ABC'+pepe+"32E26-001.xml;id=0000261090"
        print url
        exit()
    buffer = BytesIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    print 'Downloaded'
    print url
    return buffer


def main(num):
    global writer
    num = '00'+str(x) if x < 10 else '0'+str(x)

    try:
        reader = PdfFileReader(download(num))
    
    except utils.PdfReadError:
        reader = PdfFileReader(download(num))

    reader.decrypt('')
    writer.addPage(reader.getPage(0))
    print 'Added'

[main(x) for x in tqdm(range(1, 65))]
with open('heyy.pdf', 'wb') as f:
    writer.write(f)
