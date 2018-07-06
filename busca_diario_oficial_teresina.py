# coding=utf-8

import requests
import urllib2
from lxml import html
import PyPDF2
import re
import os


# PALAVRAS A SEREM BUSCADAS
palavras = ['marcelo'] 
# #########################

# QUANTIDAD DE PÁGINAS A SEREM PECORRIDAS
paginas = 30

# Cria uma pasta pdfs para armazenar os pdfs baixos
if not os.path.exists('pdfs'):
	os.makedirs('pdfs')

# Cria uma pasta founds para armazenar as paginas dos pdf que contem as palavras buscadas
if not os.path.exists('founds'):
	os.makedirs('founds')

url_address = 'lista_diario.php'
for page in range(1,paginas):
	print(u'Página {}'.format(page))
	url = requests.get('{}/{}?pagina={}'.format('http://www.dom.teresina.pi.gov.br',url_address, page))
	tree = html.fromstring(url.content)
	pdfs = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr/td/ul/li/a/@href')

	for pdf in pdfs:
		print(pdf)
		
		file_name = pdf.split('/')[-1]
		date = file_name.split('-')[1]

		year = date[4:8]
		month = date[2:4]
		day = date[0:2]
		dom = file_name.split('-')[0]
		
		year_folder = 'pdfs/{}'.format(year)
		month_folder = '{}/{}'.format(year_folder, month)
		day_folder = '{}/{}'.format(month_folder, day)

		if not os.path.exists(year_folder):
			os.makedirs(year_folder)

		if not os.path.exists(month_folder):
			os.makedirs(month_folder)

		if not os.path.exists(day_folder):
			os.makedirs(day_folder)

		local_pdf = '{}/{}'.format(day_folder,file_name)

		try:
			if not os.path.exists(local_pdf):

				response = urllib2.urlopen(urllib2.Request(pdf.replace(' ','%20'))).read()
				with open(local_pdf, "wb") as handle:
					handle.write(response)

			pdf_file = open(local_pdf)
				
			file_reader = PyPDF2.PdfFileReader(pdf_file)

			for page_number in xrange(file_reader.numPages):

				page = file_reader.getPage(page_number)
				text = page.extractText()

				for palavra in palavras:

					if re.search(palavra, text, re.IGNORECASE):
						writer = PyPDF2.PdfFileWriter()
						writer.addPage(page)
						
						# Cria um arquivo com o padrão: DOM123-01021980-1.pdf dentro da pasta founds
						outputstream = open("{}/{}-{}-{}-{}.pdf".format('founds',palavra,dom,date,page_number), "wb")
						writer.write(outputstream)
						outputstream.close()

		except urllib2.HTTPError:
				print('erro ao baixar o arquivo {}'.format(pdf))
