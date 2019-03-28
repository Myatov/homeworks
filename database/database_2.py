from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
import sqlalchemy as sa #ORM - система работы с базой данных без использования голового SQL

metadata = sa.MetaData()
connection = {'user': 'py4seo', 'database': 'library', 'host': '46.30.164.249', 'password': 'PY1111forSEO'}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)

Book = sa.Table( #создаем таблицу 
	'books_myatov', metadata,
	sa.Column('id', sa.Integer, primary_key = True), # первичный ключ, ускоряет индексацию
	sa.Column('original_id', sa.Integer),
	sa.Column('name', sa.String(255)),
	sa.Column('description', sa.Text),
	sa.Column('book_details', sa.Text),
	sa.Column('comments', sa.Text),
	sa.Column('pages_num', sa.Integer),
	sa.Column('genres', sa.String(255)),
	sa.Column('alias', sa.String(255)),
	sa.Column('image', sa.String(255)),
	sa.Column('date', sa.Date),
	sa.Column('processed', sa.Boolean)
)



def worker(qu):
	engine = sa.create_engine(dsn)
	conn = engine.connect()
	session = HTMLSession()
	while qu.size()>0:
		try:
			url = qu.get()
			resp = session.get(url)
			title = resp.html.xpath('//title/text()')[0]
			title = title.strip()
			conn.execute(Book.create().value(description=title))
			print (title)
			new_links = resp.html.absolute_links
			for ln in new_links:
				qu.put(url)
		except Exception as e:
			print (type(e), e)

def main():
	domain = input ('Enter domain name: ')
	home_url = f'http://{domain}/'
	session = HTMLSession()

	q = Queue()
	resp = session.get(home_url)
	new_links = resp.html.absolute_links
	for ln in new_links:
		q.put(ln)

	print (q.qsize())

	executor = ThreadPoolExecutor(max_workers=10)
	for _ in range(10):
		executor.submit(worker, q)

main()