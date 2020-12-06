from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://postgres:qwerty21qwerty@localhost:5432/Library')
Base = declarative_base()

class Reader(Base):
    __tablename__ = 'Readers'
    
    reader_id = Column(Integer, primary_key=True)
    fullname = Column(String)
    address = Column(String)
    age = Column(Integer)
    
    subscriptions = relationship('Subscription')
    
    def __init__(self, fullname=None, address=None, age=None):
        self.fullname = fullname
        self.address = address
        self.age = age
        
class Author(Base):
    __tablename__ = 'Authors'
    
    author_id = Column(Integer, primary_key=True)
    fullname = Column(String)
    birth_date = Column(Date)
    country = Column(String)
    
    authors_books = relationship('Authors_books')
    
    def __init__(self, fullname=None, birth_date=None, country=None):
        self.fullname = fullname
        self.birth_date = birth_date
        self.country = country

class Book(Base):
    __tablename__ = 'Books'
    
    book_id = Column(Integer, primary_key=True)
    name = Column(String)
    publish_date = Column(Date)
    quantity = Column(Integer)
    
    authors_books = relationship('Authors_books')
    books_subscriptions = relationship('Books_subscriptions')
    
    def __init__(self, name=None, publish_date=None, quantity=None):
        self.name = name
        self.publish_date = publish_date
        self.quantity = quantity
        
class Subscription(Base):
    __tablename__ = 'Subscriptions'
    
    subscription_id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    reader_id = Column(Integer, ForeignKey('Readers.reader_id'))
    type = Column(String)
    
    books_subscriptions = relationship('Books_subscriptions')
    
    def __init__(self, start_date=None, end_date=None, reader_id=None, type=None):
        self.start_date = start_date
        self.end_date = end_date
        self.reader_id = reader_id
        self.type = type
        
class Authors_books(Base):
    __tablename__ = 'Authors_books'
    
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('Authors.author_id'))
    book_id = Column(Integer, ForeignKey('Books.book_id'))
    
    def __init__(self, author_id=None, book_id=None):
        self.author_id = author_id
        self.book_id = book_id
        
class Books_subscriptions(Base):
    __tablename__ = 'Books_subscriptions'
    
    books_subscriptions_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('Books.book_id'))
    subscription_id = Column(Integer, ForeignKey('Subscriptions.subscription_id'))
    
    
    def __init__(self, book_id=None, subscription_id=None):
        self.book_id = book_id
        self.subscription_id = subscription_id
        
session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'Readers': Reader, 'Authors': Author, 'Books': Book, 'Subscriptions': Subscription, 'Authors_books': Authors_books, 'Books_subscriptions': Books_subscriptions}  

class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}
        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def insert(self, tname, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[tname]
        obj = object_class(**pairs)

        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, tname, condition):
        try:
            pairs = self.pairs_from_str(condition)
        except Exception as err:
            raise Exception('Incorrect input')
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, tname, condition, statement):
        try:
            pairs = self.pairs_from_str(condition)
            new_values = self.pairs_from_str(statement)
        except Exception as err:
            raise Exception('Incorrect input')

        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)
                
    def fill_readers_table_with_random_data(self):
        sql = """
            CREATE OR REPLACE FUNCTION randomReaders()
                RETURNS void AS $$
            DECLARE
                step integer := 10;
            BEGIN
                LOOP EXIT WHEN step > 1000;
                    INSERT INTO public."Readers" (fullname, address, age)
                    VALUES (
                        substring(md5(random()::text), 1, 10),
                        substring(md5(random()::text), 1, 10),
                        (random() * (90 - 1) + 1)::integer
                    );
                step := step + 1;
            END LOOP;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomReaders();
        """
        try:
            session.execute(sql)
        finally:
            session.commit()
