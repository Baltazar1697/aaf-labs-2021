# DB structure

class db:
    def __init__(self):
        self._tables = {}
    def __getitem__(self, name):
        return self._tables[name]
    def __setitem__(self, key, value):
        self._tables[key] = value
    @staticmethod
    def check_columns(self, columns: list, table_name) -> bool: # Check if columns are in table
        if len(columns) != len(self[table_name]._scheme.keys()):
            return False
        return True

    def create(self, table_name: str, columns: list) -> str: # Create table
        if columns:
            scheme = {}
            for i in columns:
                scheme[i] = columns[i]
            self[table_name] = table(table_name, scheme)
            return f"Table '{table_name}' has been created!"
        return "invalid columns!"

    def insert(self, table_name: str, values: list) -> str: # Insert into table
        indexator_value = values[self[table_name]._indexator]
        self[table_name][indexator_value] = {}
        if self.check_columns(self, values, table_name):
            for i in range(self[table_name].__len__()):
                self[table_name][indexator_value][list(self[table_name]._scheme.keys())[i]] = values[i]

            return f"{values} has been inserted!"
        else:
            return f"Incorrect input! Try again!"

    def select_valuer(self, value: str, index, keys: list, table_name: str):
        print('|', end='')
        if value == 'keys':
            if len(keys) == 1 and keys[0] == '*':
                for key in self[table_name]._scheme:
                    print(' ' + key + ' |', end='')
            else:
                for key in keys:
                    print(' ' + key + ' |', end='')
        elif value =='data':
            print(' '+ str(list(self[table_name]._data.keys())[index]) +' |', end='')
            for i in self[table_name]._data:
                for j in range(1,len(self[table_name]._data[i].values())):
                    print(' ',str(list(self[table_name]._data[i].values())[j])+ ' |', end='')
            print()
    def select_liner(self, keys, table_name: str):
        if len(keys) == 1 and keys[0] == '*':
            for key in self[table_name]._scheme:
                string = '+'+'-'*(2+len(key))
                print(string, end='')
        else:
            string = '+'+'-'*(2+len(str(list(self[table_name]._scheme.keys())[0])))
            print(string, end='')
            for key in keys:
                string = '+'+'-'*(2+len(key))
                print(string, end='')
#
    def select_valuer_spec(self, value: list, index, table_name: str):
        print('|', end='')
        print(' '+ str(list(self[table_name]._data.keys())[index]) + ' |', end='')
        for i in self[table_name]._data:
            for j in value:
                print(' ', str(self[table_name]._data[i][j]) + ' |', end='')

    def select(self, table_name: str, columns: list, condition: list,) -> str: # Return columns selected
        if len(columns) == 1 and columns[0] == "*":
            self.select_liner('*', table_name)
            print('+')
            self.select_valuer('keys', 0, table_name)
            print()
            self.select_liner('*', table_name)
            print()
            for i in range(self[table_name].dict_len()):
                self.select_valuer('data', i, table_name)
                self.select_liner('*', table_name)
            print()
        else:
            self.select_liner(columns, table_name)
            print('+')
            print('| '+ str(list(self[table_name]._scheme.keys())[0])+ ' ', end='')
            self.select_valuer('keys', 0, columns, table_name)
            print()
            self.select_liner(columns, table_name)
            print()
            for i in range(self[table_name].dict_len()):
                self.select_valuer_spec(columns, i, table_name)
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