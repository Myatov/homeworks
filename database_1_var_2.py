import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
# https://developers.google.com/webmaster-tools/search-console-api-original/v3/quickstart/quickstart-python
# https://developers.google.com/api-client-library/python/apis/webmasters/v3


Base = declarative_base()
Session = sessionmaker()

connection = {'user': 'py4seo', 'database': 'library', 'host': '46.30.164.249', 'password': 'PY1111forSEO'}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)
engine = sa.create_engine(dsn, echo=True) #echo=True - дебаг режим
Base.metadata.bind = engine

Session.configure(bind=engine)
session = Session()

table_name = 'books_myatov_2'

class Book(Base): #sqlalchemy

	__tablename__ = table_name

	id = sa.Column(sa.Integer, primary_key = True)
	name = sa.Column(sa.String(255))
	author_id = sa.Column(sa.Integer, sa.ForeignKey('books_authors_myatov_2.id'))
	author = sa.orm.relationship('Author', back_populates = 'books')
	# processed = sa.Column(sa.Boolean)


class Author(Base):

	__tablename__ = 'books_authors_myatov_2'

	id = sa.Column(sa.Integer, primary_key = True)
	name = sa.Column(sa.String(255))
	books = sa.orm.relationship('Book', back_populates = 'author')


if __name__ == '__main__':
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

war = Book(name = 'War and Peace')
author = Author(name = 'Leo Tolstoy')
war.author = author

anna = Book(name = 'Anna Karenina', author = author)
childhodd = Book(name = 'Childhodd', author = author)
session.add(war)
session.add(anna)
session.add(childhodd)
session.commit()

# [book.name for book in author.books]
for res in session.query(Book, Book.name):
	print (res)

auth = session.query(Author).first()
auth.name = auth.name.replace('Leo', 'Lev')
session.add(auth)
session.commit()

session.query(Book).count() #число книг в базе

