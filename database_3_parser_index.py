from requests_html import HTMLSession
from reppy.robots import Robots
from database_3_parser_config import sa, AllData, engine

print ('Start working')

domain = input ('Enter domain name: ')

url = f'http://{domain}/'
robots_url = f'http://{domain}/robots.txt'

robots = Robots.fetch(robots_url)

links_to_scan = set()
links_to_scan.add(url)

scaned_links = set()

session = HTMLSession()

conn = engine.connect()


class URLData:

	def __init__ (self, url_url, url_title, url_description, ulr_h1, url_canonical):
		self.url_url = [url]
		self.url_title = title
		self.url_description = description
		self.url_h1 = h1
		self.url_canonical = canonical
		print (f'{self.url_url}, {self.url_title}, {self.url_description}, {self.url_h1}, {self.url_canonical})

while len (links_to_scan) > 0:
	url = links_to_scan.pop()
	scaned_links.add(url)

	if not robots.allowed(url, '*'):
		continue

	try:
		print ('SEND REQUEST TO: ', url)
		resp = session.get(url)
		links = resp.html.absolute_links
		print (f'Found {len(links)} links.')

		title = resp.html.xpath('//title/text()')
		description = resp.html.xpath('//meta[@name="description"]/@content')
		h1 = resp.html.xpath('//h1/text()')
		canonical = resp.html.xpath('//meta[@name="canonical"]/@rel')

		page = URLData(url, title, description, h1, canonical)

		url = page.url_url
		title = page.url_title
		description = page.url_description
		h1 = page.url_h1
		canonical = page.url_canonical

		book_values = {
			'url': page.url_url,
			'title': page.url_title,
			'description': page.url_description,
			'h1': page.url_h1,
			'canonical': page.url_canonical
		}
		query = AllData.insert().values(**book_values)
		conn.execute(query)

		links_to_scan = links.links_to_scan.union(links) - scaned_links
		print (f'Links to scan: {len(links_to_scan)}')
	except:
		print(type(e), e)

print ('All Done!')