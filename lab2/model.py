import os
import psycopg2

class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432", database='Library', user='postgres', password='qwerty21qwerty')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to PostgreSQL', error)

    def get_column_names(self):
        return [d[0] for d in self.cursor.description]

    def create_data_base(self):
        f = open('library.txt', 'r')
        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, table_name, param, arg):
        try:
            query = f'SELECT {param} FROM public."{table_name}"'
            if arg:
                query += ' WHERE ' + arg
            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, table_name, columns, values):
        try:
            query = f'INSERT INTO public. "{table_name}" ({columns}) VALUES ({values});'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, table_name, condition):
        try:
            query = f'DELETE FROM public. "{table_name}" WHERE {condition};'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, table_name, value, new_value):
        try:
            query = f'UPDATE public. "{table_name}" SET {new_value} WHERE {value}'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def filter_books_table(self, name, author_fullname, author_country):
        query = f"""
        SELECT b.name, a.country, a.fullname
        FROM public."Books" b
        INNER JOIN public."Authors_books" l ON b.book_id=l.book_id
        INNER JOIN public."Authors" a ON l.author_id=a.author_id
        """
        if name:
            query += f'\nWHERE name LIKE\'%{name}%\''
        if author_fullname and not name:
            query += f'\nWHERE fullname LIKE \'%{author_fullname}%\''
        elif author_fullname:
            query += f' AND fullname LIKE \'%{author_fullname}%\''
        if author_country and not name and not author_fullname:
            query += f'\nWHERE country LIKE \'%{author_country}%\''
        elif author_country:
            query += f' AND country LIKE \'%{author_country}%\''
        try:
            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fill_readers_table_with_random_data(self, quantity):
        sql = f"""
        CREATE OR REPLACE FUNCTION randomReaders()
            RETURNS void AS $$
        DECLARE
            step integer := 1;
        BEGIN
            LOOP EXIT WHEN step > {quantity};
                INSERT INTO public."Readers" (fullname, address)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 10)
                );
                step := step + 1;
            END LOOP;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomReaders();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()