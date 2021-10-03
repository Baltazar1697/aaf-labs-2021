from typing import List
import db, re


class Parser:
    def __init__(self):                         #initial action for start of the application
        while True:
            query = input('--> ')
            for command in query.split(';'):    #split commands with ';' : CREATE ...; SELECT ... 
                if command:                     # => in dif. commands
                    print (self.action(query))
        
    def action(self, query:str) -> str:         #TODO: optimize this shit
        query = self.parse_command(query)       #split input command to the list with needed arguments
        command = query[0]
        print (query)
        if command == 'CREATE':
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

    def parse_command(self, query) -> list:     #splits input for list of [command, column, values, *arg]
        str = re.findall(r'\S+', query)
        for i in str:
            if i.upper() == 'CREATE' and str.index(i)+1 < len(str):
                columns = {}
                table_name = str[str.index(i)+1] # if str[0] == CREATE => str[1] = table_name
                m = query.split('(', 1)[1].split(')')[0].replace(',', '').split()   #parse arguments
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