from consolemenu import SelectionMenu
from view import View
from model import Model

TABLES_NAMES = ['Authors', 'Books', 'Authors_books', 'Readers', 'Subscriptions', 'Book_subscription_links']
TABLES = {
    'Authors':['author_id', 'fullname', 'birth_date', 'country'],
    'Books':['book_id', 'name', 'publish_date', 'quantity'],
    'Authors_books':['id', 'author_id', 'book_id'],
    'Readers':['reader_id', 'fullname', 'address'],
    'Subscriptions':['subscription_id', 'start_date', 'end_date', 'reader_id'],
    'Book_subscription_links':['id', 'book_id', 'subscription_id']
}

def get_input(table_name=''):
    if table_name:
        print(' '.join(TABLES[table_name]), end='\n\n')
    return input()

def get_insert_input(table_name):
    print(' '.join(TABLES[table_name]), end='\n\n')
    return input(), input()

def press_enter():
    input()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_start_menu(self, input=''):
        selection_menu = SelectionMenu(
            TABLES_NAMES + ['Find books by name or author`s fullname',
            'Fill the Readers (random)'],
            title = 'Input:',
            subtitle=input)

        selection_menu.show()
        option = selection_menu.selected_option
        if option < len(TABLES_NAMES):
            table_name = TABLES_NAMES[option]
            self.show_entity_menu(table_name)
        elif option == 6:
            self.filter_books()
        elif option == 7:
            self.random_data_for_readers_table()
        else:
            print('')

    def show_entity_menu(self, table_name, input=''):
        options = ['GET', 'INSERT', 'DELETE', 'UPDATE']
        methods = [self.get, self.insert, self.delete, self.update]

        selection_menu = SelectionMenu(options,
        f'Table: {table_name}',
        exit_option_text = 'Back',
        subtitle = input)
        selection_menu.show()

        try:
            method = methods[selection_menu.selected_option]
            method(table_name)
        except IndexError:
            self.show_start_menu()

    def get(self, table_name):
        try:
            data = self.model.get(table_name, '*', '')
            self.view.print_data(data)
            press_enter()
            self.show_entity_menu(table_name)
        except Exception as error:
            self.show_entity_menu(table_name, str(error))

    def insert(self, table_name):
        try:
            print(f'Insert into the {table_name}...\nEnter columns (column1) - enter - and values (\'value1\') divided with commas.')
            columns, values = get_insert_input(table_name)
            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Successfully inserted!')
        except Exception as error:
            self.show_entity_menu(table_name, str(error))

    def delete(self, table_name):
        try:
            print(f'Delete from the {table_name}...\nEnter condition (SQL):')
            condition = get_input(table_name)
            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Successfully deleted!')
        except Exception as error:
            self.show_entity_menu(table_name, str(error))

    def update(self, table_name):
        try:
            print(f'Update the {table_name}...\nEnter condition (SQL):')
            condition = get_input(table_name)
            print('Enter what to update (key=\'value\'):')
            to_update = get_input(table_name)
            self.model.update(table_name, condition, to_update)
            self.show_entity_menu(table_name, 'Successfully updated!')
        except Exception as error:
            self.show_entity_menu(table_name, str(error))

    def filter_books(self):
        try:
            print('Enter a books name or leave empty:')
            books_name = get_input()
            print('Enter a books author fullname or leave empty:')
            books_author_fullname = get_input()
            print('Enter a books author`s country or leave empty:')
            author_country = get_input()
            data = self.model.filter_books_table(books_name, books_author_fullname, author_country)
            self.view.print_data(data)
            press_enter()
            self.show_start_menu()
        except Exception as error:
            self.show_start_menu(str(error))

    def random_data_for_readers_table(self):
        try:
            print('Fill the Reader with random data...\nEnter quantity to be generated:')
            readers_quantiy = get_input()
            self.model.fill_readers_table_with_random_data(readers_quantiy)
            self.show_start_menu('Successfully generated random Readers!')
        except Exception as error:
            self.show_start_menu(str(error))