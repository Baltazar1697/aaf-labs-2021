def create(table_name, columns):
    DB = database(table_name, columns)
    print ('Table', table_name, 'has been created with columns ', columns)
    return DB

def select(table_name, columns):
    print ('SELECTED',columns, ' FROM ', table_name)
    
def insert(table_name, values):
    print ('Inserted row with ', values, ' in ', table_name)

def delete(table_name):
    print ('Deleted ', table_name)
        
class database:
    def __init__(self, table_name, columns) -> None:
        self.table_name = table_name
        self.tables = columns

