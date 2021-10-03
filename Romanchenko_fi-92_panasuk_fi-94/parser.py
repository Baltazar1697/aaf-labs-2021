from typing import List
import db, re


class Parser:
    def __init__(self):
        while True:
            query = input('--> ')
            for command in query.split(';'):
                if command:
                    print (self.action(query))
        
    def action(self, query:str) -> str:
        command = query.split()[0].upper()
        query = self.parse_command(query)
        if command == 'CREATE':
            print (query)
            _, table_name, columns = query
            
            action_call = db.create(table_name, columns)
        elif command == 'SELECT':
            _, table_name = query
            action_call = db.select(table_name)
        elif command == 'INSERT':
            _, table_name, values = query
            action_call = db.insert(table_name, values)
        elif command == 'DELETE':
            _, table_name = query
            action_call = db.delete(table_name)
        else:
            action_call = self.error()

        return action_call

    def error(self):
        return 'ERROR, COMMAND NOT FOUND'

    def parse_command(self, query) -> list:
        str = re.findall(r'\S+', query)
        columns = {}
        print (str)
        for i in str:
            if i.upper() == 'CREATE' and str.index(i)+1 < len(str):
                table_name = str[str.index(i)+1]
                m = query.split('(', 1)[1].split(')')[0].replace(',', '').split()
                for column in m:
                    if column == 'INDEXED':
                        pass
                    elif column == m[-1] or m[m.index(column)+1] != 'INDEXED':
                        columns[column] = False
                    elif m[m.index(column)+1] == 'INDEXED':
                        columns[column] = True
                    
                return ['CREATE', table_name, columns]

if __name__ == '__main__':
    client = Parser()
# parser(query_test_2)
# parser(query_test_1)5