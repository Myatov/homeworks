import sqlalchemy as sa

table_name = 'parser_myatov'

metadata = sa.MetaData()
connection = {'user': 'py4seo', 'database': 'library', 'host': '46.30.164.249', 'password': 'PY1111forSEO'}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)
engine = sa.create_engine(dsn)
metadata.bind = engine

AllData = sa.Table(
	'parser_myatov', metadata,
	sa.Column('id', sa.Integer, primary_key = True),
	sa.Column('url', sa.String(255)),
	sa.Column('title', sa.String(255)),
	sa.Column('description', sa.Text),
	sa.Column('h1', sa.String(255)),
	sa.Column('canonical', sa.String(255)),
)

if __name__ == '__main__':
	#metadata.drop_all(engine)
	metadata.create_all()