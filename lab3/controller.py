from consolemenu import SelectionMenu

from view import View
from model import Model

TABLES_NAMES = ['Authors', 'Books', 'Authors_books', 'Readers', 'Subscriptions', 'Book_subscription_links']
TABLES = {
    'Authors':['author_id', 'fullname', 'birth_date', 'country'],
    'Books':['book_id', 'name', 'publish_date', 'quantity'],
    'Authors_books':['id', 'author_id', 'book_id'],
    'Readers':['reader_id', 'fullname', 'address', 'age'],
    'Subscriptions':['subscription_id', 'start_date', 'end_date', 'reader_id', 'type'],
    'Book_subscription_links':['id', 'book_id', 'subscription_id']
}

def get_input(msg, table_name=''):
    print(msg)
    if table_name:
        print(' | '.join(TABLES[table_name]), end='\n\n')
    return input()

def get_insert_input(msg, table_name):
    print(msg)
    print(' | '.join(TABLES[table_name]), end='\n\n')
    return input(), input()

def press_enter():
    input()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_start_menu(self, msg=''):
        selection_menu = SelectionMenu(
            TABLES_NAMES + ['Fill the Readers (random)', 'Commit'],
            title='Select the table to work with | command:', subtitle=msg)
        selection_menu.show()

        index = selection_menu.selected_option
        if index < len(TABLES_NAMES):
            table_name = TABLES_NAMES[index]
            self.show_entity_menu(table_name)
        elif index == len(TABLES_NAMES):
            self.random_data_for_readers_table()
        elif index == len(TABLES_NAMES) + 1:
            self.model.commit()
            self.show_start_menu(msg='Commit success')
        else:
            print(' ')

    def show_entity_menu(self, table_name, input=''):
        options = ['INSERT', 'DELETE', 'UPDATE']
        methods = [self.insert, self.delete, self.update]

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

    def insert(self, table_name):
        try:
            columns, values = get_insert_input(
                f"INSERT {table_name}\nEnter columns divided with commas, then do the same for values in format: [value1, value2, ...]",
                table_name)
            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def delete(self, table_name):
        try:
            condition = get_input(
                f'DELETE {table_name}\n Enter condition (SQL):', table_name)
            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def update(self, table_name):
        try:
            condition = get_input(
                f'UPDATE {table_name}\nEnter condition (SQL):', table_name)
            statement = get_input(
                "Enter SQL statement in format [<key>=<value>]", table_name)
            self.model.update(table_name, condition, statement)
            self.show_entity_menu(table_name, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def random_data_for_readers_table(self):
        try:
            self.model.fill_readers_table_with_random_data()
            self.show_start_menu('Successfully generated 1000 random Readers!')
        except Exception as err:
            self.show_init_menu(str(err))