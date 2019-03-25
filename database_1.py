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

if __name__ == '__main__':
	engine = sa.create_engine(dsn)
	#metadata.drop_all(engine)
	metadata.create_all(engine)