# DB structure

class db:
    @staticmethod
    def check_columns(self, columns: list) -> bool: # Check if columns are in table
        for column in columns:
            if column not in self._table._scheme.keys():
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
        if self.check_columns(self, values):
            for i in values:
               1
        return f"{values} has been inserted!"

    def select(self, table_name: str, columns: list, condition: list,) -> str: # Return columns selected
        return f"{len(columns)} row(s) has been selected from {table_name} with {condition}!"

    def delete(self, table_name: str, condition: list) -> str: # Delete data from table
        return f"From {table_name} row(s) has been deleted from {table_name}!"

if __name__ == "__main__":
    db = db()

class table:
    def __init__(self, table_name, scheme):
        self._table_name = table_name
        self._indexator = list(scheme.keys())[list(scheme.values()).index(True)]
        self._scheme = scheme
        self._data = {}
        print(self._indexator)
        print(self._scheme.keys())

        def __getitem__(self, item):
            return self._data[item]

