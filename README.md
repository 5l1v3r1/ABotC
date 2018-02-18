#ABotC

Herramienta para descargar, en formato PDF, los ejemplares del archivo histórico del diario ABC correspondientes al período especificado.

##Instrucciones de uso: 
'''  
abc2.py -s yyyy-mm-dd -e yyyy-mm-dd
''' 
Argumentos:
    -s: fecha de inicial
    -e: fecha de final

##Requisitos
Para poder ejecutar correctamente el script los siguientes módulos son necesarios:
###Networking
* [PyCurl](http://pycurl.io/)
* [Requests](http://docs.python-requests.org/en/master/)
###Manejo de pdf
* [PyPDF2](https://github.com/mstamy2/PyPDF2)
###WebScrapping
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
###Otros
* [io](https://docs.python.org/2/library/io.html)
* [Subprocess](https://docs.python.org/2/library/subprocess.html)

##Úsese con responsabilidad. El autor no se responsabiliza del uso indebido que los usuarios finales hagan de esta herramienta