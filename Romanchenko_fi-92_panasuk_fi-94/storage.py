# DB structure

class db:
    @staticmethod
    def check_columns(self, table_name: str, columns: list) -> bool: # Check if columns are in table
        for column in columns:
            if column not in self.tables[table_name].columns:
                return False
        return True

    def create(self, table_name: str, columns: list) -> str: # Create table
        if columns:
            # Add dunction of creating table
            return f"Table '{table_name}' has been created!"
        return "invalid columns!"

    def insert(self, table_name: str, values: list) -> str: # Insert into table
        return f"{len(values)} row(s) has been inserted into {table_name}!"

    def select(self, table_name: str, columns: list, condition: list,) -> str:
        return f"{len(columns)} row(s) has been selected from {table_name} with {condition}!"

    def delete(self, table_name: str, condition: list) -> str:
        return f"From {table_name} row(s) has been deleted from {table_name}!"

if __name__ == "__main__":
    db = db()