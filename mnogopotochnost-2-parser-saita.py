#пишем многопоточный парсер сайта

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession


def worker (qu):
	session = HTMLSession()
	while qu.size > 0:
		url = qu.get()
		resp = session.get(url)
		print(resp.html.xpath('//title/text()')[0])
		new_links = resp.html.absolute_links
		for ln in new_links:
			qu.put(ln)


def main():
	domain = input('Enter domain name: ')
	home_url = f'https://{domain}/'
	session = HTMLSession()

	q = Queue()
	resp = session.get(home_url)
	new_links = resp.html.absolute_links
	for ln in new_links:
		q.put(ln)

	print (q.qsize())

	executor = ThreadPoolExecutor(max_workers = 10)
	for _ in range(10):
		executor.submit(worker, q)

main()