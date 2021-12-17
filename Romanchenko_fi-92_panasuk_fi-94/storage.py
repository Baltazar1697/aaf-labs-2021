# DB structure

class db:
    @staticmethod
    def check_columns(self, columns: list) -> bool: # Check if columns are in table
        if len(columns) != len(self._table._scheme.keys()):
            return False
        return True

    def create(self, table_name: str, columns: list) -> str: # Create table
        if columns:
            scheme = {}
            for i in columns:
                scheme[i] = columns[i]
            self._table = table(table_name, scheme)
            return f"Table '{table_name}' has been created!"
        return "invalid columns!"

    def insert(self, table_name: str, values: list) -> str: # Insert into table
        indexator_value = values[self._table._indexator]
        self._table._data[indexator_value] = {}
        if self.check_columns(self, values):
            for i in range(self._table.__len__()):
                self._table._data[indexator_value][list(self._table._scheme.keys())[i]] = values[i]

            return f"{values} has been inserted!"
        else:
            return f"Incorrect input! Try again!"

    def select_valuer(self, value: str, index, keys: list):
        print('|', end='')
        if value == 'keys':
            if len(keys) == 1 and keys[0] == '*':
                for key in self._table._scheme:
                    print(' ' + key + ' |', end='')
            else:
                for key in keys:
                    print(' ' + key + ' |', end='')
        elif value =='data':
            print(' '+ str(list(self._table._data.keys())[index]) +' |', end='')
            for i in self._table._data:
                for j in range(1,len(self._table._data[i].values())):
                    print(' ',str(list(self._table._data[i].values())[j])+ ' |', end='')
            print()
    def select_liner(self, keys):
        if len(keys) == 1 and keys[0] == '*':
            for key in self._table._scheme:
                string = '+'+'-'*(2+len(key))
                print(string, end='')
        else:
            string = '+'+'-'*(2+len(str(list(self._table._scheme.keys())[0])))
            print(string, end='')
            for key in keys:
                string = '+'+'-'*(2+len(key))
                print(string, end='')
#
    def select_valuer_spec(self, value: list, index):
        print('|', end='')
        print(' '+ str(list(self._table._data.keys())[index]) + ' |', end='')
        for i in self._table._data:
            for j in value:
                print(' ', str(self._table._data[i][j]) + ' |', end='')

    def select(self, table_name: str, columns: list, condition: list,) -> str: # Return columns selected
        if len(columns) == 1 and columns[0] == "*":
            self.select_liner('*')
            print('+')
            self.select_valuer('keys', 0)
            print()
            self.select_liner('*')
            print()
            for i in range(self._table.dict_len()):
                self.select_valuer('data', i)
                self.select_liner('*')
            print()
        else:
            self.select_liner(columns)
            print('+')
            print('| '+ str(list(self._table._scheme.keys())[0])+ ' ', end='')
            self.select_valuer('keys', 0, columns)
            print()
            self.select_liner(columns)
            print()
            for i in range(self._table.dict_len()):
                self.select_valuer_spec(columns, i)
            print()
        return f"{len(columns)} row(s) has been selected from {table_name} with {condition}!"

    def delete(self, table_name: str, condition: list) -> str: # Delete data from table
        return f"From {table_name} row(s) has been deleted from {table_name}!"

if __name__ == "__main__":
    db = db()

class table:
    def __init__(self, table_name, scheme):
        self._table_name = table_name
        self._indexator = list(scheme.values()).index(True)
        self._scheme = scheme
        self._data = {}
        print(self._indexator)
        print(self._scheme.keys())

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
    def __len__(self):
        return len(self._scheme.keys())
    def dict_len(self):
        return len(self._data)