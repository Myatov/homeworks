from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
import re

pages = set()

def get_domain(domain_name):
	"""
	приводим домен к нужному виду. Кто его знает, что введёт пользователь
	"""
	domain_not_url = domain_name.split('//')[-1].split('www.')[-1].split('/')[0].strip()
	if 'http' not in domain_name:
		domain_url = 'http://' + domain_not_url
	else:
		domain_url = domain_name.strip()
	return domain_not_url, domain_url

def get_data(page_url):
	"""
	функция получения данных с конкретной страницы
	"""
	result_pars = {}
	session = HTMLSession()
	resp = session.get(page_url)
	if resp.status_code == 200:
		soup = BeautifulSoup(resp.text, 'lxml') #пришлось использовать для универсальности

		try:
			result_pars['title'] = soup.find('title').text
		except Exception:
			result_pars['title'] = ''

		try:
			result_pars['h1'] = soup.find('h1').text
		except Exception:
			result_pars['h1'] = ''

		#вытаскиваем description
		desc = ''
		try:
			for meta in soup.findAll('meta'):
				metaname = meta.get('name', '').lower()
				metaprop = meta.get('property', '').lower()
				if 'description' == metaname or metaprop.find('description') > 0:
					desc = meta['content'].strip()
			result_pars['description'] = desc
		except Exception:
			result_pars['description'] = ''

		csv_writer(page_url, result_pars)

def get_links(page_url, domain_data):
	"""
	Основная функция с рекурсией
	"""
	pictures = ['.jpg', '.jpeg', '.gif', '.png', '.pdf', '.doc']
	global pages
	session = HTMLSession()
	resp = session.get(page_url)

	if resp.status_code == 200:
		try:
			links = resp.html.absolute_links
			links = [x for x in links if re.search(f'.*://{domain_data}/', x)]
		except Exception:
			print ('Не удалось получить ссылки домена.')

		for link in links:
			if link not in pages:
				#если ссылка на картинку, то пропускаем её
				if [x for x in pictures if x in link]:
					pages.add(link)
					continue
				get_data (link)
				new_page = link
				pages.add(new_page)
				get_links(new_page, domain_data)
	else:
		print ('Страница не доступна')
		return None

def csv_writer(page_url, data_csv):
	"""
	Функция чтения и записи в файл
	"""
	global domain
	data_read = []

	with open(domain + '.csv', 'a+', newline='') as file:
		writer = csv.writer(file, delimiter = ';')
		reader = csv.reader(file, delimiter = ';')
		file.seek(0)
		for row in reader:
			data_read = row

		if data_read:
			if [x for x in data_read[1:4] if x in data_csv.values()]:
				file.seek(2)
				writer.writerow((page_url, data_csv['title'], data_csv['description'], data_csv['h1']))
				print ('Записали строку в файл с дублем')
			else:
				file.seek(2)
				writer.writerow((page_url, data_csv['title'], data_csv['description'], data_csv['h1']))
				print ('Записали строку в файл')
		else:
			file.seek(2)
			writer.writerow((page_url, data_csv['title'], data_csv['description'], data_csv['h1']))
			print ('Записали первую строку в файл')

domain = input('Введите доменное имя или exit: ')
domain, url_domain = get_domain(domain)
get_links (url_domain, domain)
print ('Парсинг сайта завершен.')

print ('== ПОКА ==')