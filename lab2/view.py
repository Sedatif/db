class View:
    def print_data(self, data):
        columns, rows = data
        line_length = 30 * len(columns)

        self.print_separator(line_length)
        self.print_row(columns)
        self.print_separator(line_length)

        for row in rows:
            self.print_row(row)

        self.print_separator(line_length)

    def print_row(self, row):
        for column in row:
            print(str(column).rjust(26, ' ') + '  |', end='')
        print('')

    def print_separator(self, length):
        print('-' * length)