import pdb
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
frob db import Book, sa, dsn

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-US;q=0.6,en;q=0.4",
	"Cache-control": "max-age=0",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}

def worker(urls_q):
	engine = sa.create_engine(dsn)
	conn = engine.connect()
	session = HTMLSession()
	while urls_q.qsize() > 0:
		try:
			#pdb.set_trace()
			url = urls_q.get()
			resp = session.get(url, headers=headers)

			original_id = url.split('/')[-1]
			original_id = int(original_id.split('-')[0])
			name = resp.html.xpath('//h1[@id="bookTitle"/text()')[0]
			name = name.strip()

			description = resp.html.xpath(
				"//span[contains(@id, 'freeText') and not(contains(@id, 'freeTextContainer'))]"
				)[0].text

			genres = resp.html.xpath(
				"//div[@class='left']/a[contains(@class, 'bookPageGenreLink')]"
				)
			genres = [x.text for x in genres]

			genres = ','.join(genres)

			conn.execute(Book.insert().values(
				original_id = original_id,
				name = name,
				description = description,
				genres = genres
				)
			)
			print (name)
		except Exception as e:
			print (type(e), e)

def main():
	q = Queue()
	for i in range(10000, 100145): #будем сканировать книги в этом диапазоне
		url = f'https://www.goodreads.com/book/show/{i}-asdasda-sdqwe'
		q.put(url)

	print (q.qsize())

	executor = ThreadPoolExecutor(max_workers = 100)
	for _ in range(100):
		executor.submit(worker, q)

if __name__ == '__main__':
	main()