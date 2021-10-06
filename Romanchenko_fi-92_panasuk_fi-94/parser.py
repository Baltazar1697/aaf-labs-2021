import storage, re

class Parser:
    def __init__(self):                         #initial action for start of the application
        while True:
            query = input('--> ')
            for command in query.split(';'):    #split commands with ';' : CREATE ...; SELECT ... 
                if command:                     # => in dif. commands
                    self.action(command)
        
    def action(self, query:str) -> str:         #TODO: optimize this shit
        query = self.parse_command(query)       #split input command to the list with needed arguments
        command = query[0]

        if command == 'CREATE':
            _, table_name, columns = query
            action_call = storage.create(table_name, columns)
        elif command == 'SELECT':
            _, table_name, columns = query
            action_call = storage.select(table_name, columns)
        elif command == 'INSERT':
            _, table_name, values = query
            action_call = storage.insert(table_name, values)
        elif command == 'DELETE':
            _, table_name = query
            action_call = storage.delete(table_name)
        else:
            action_call = self.error()

        return action_call

    def error(self):
        return 'ERROR, COMMAND NOT FOUND'

    def parse_command(self, query) -> list:     #splits input for list of [command, column, values, *arg]
        str = re.findall(r'\S+', query)
        command = str[0]

        columns = {}
        table_name = str[str.index(command)+1] # if str[0] == CREATE => str[1] = table_name
        
        values = self.splitter(query)


        if command.upper() == 'CREATE':
            try:
                if len(str) < 3: raise Exception('too short')
            except:
                print('The list is too short')
                return [0]

            for column in values:
                if column == 'INDEXED':
                    pass
                elif column == values[-1] or values[values.index(column)+1] != 'INDEXED':   #TODO: regular expression for 'INDEXED'
                    columns[column] = False
                elif values[values.index(column)+1] == 'INDEXED':
                    columns[column] = True

            return ['CREATE', table_name, columns]

        elif command.upper() == 'SELECT':
            selected = str[1]
            table_name = str[str.index('FROM')+1]       #TODO: regular expresion for 'FROM'
                
            return ['SELECT', table_name, selected]

        elif command.upper() == 'INSERT':
            table_name = str[1]
            values = query.split('(', 1)[1].split(')')[0].replace(',', '').split()

            return ['INSERT',table_name, values]

        elif command.upper() == 'DELETE':
            table_name = str[str.index('FROM')+1]

            return ['DELETE', table_name]

    def splitter(self, query):
        #// CATCH input without brackets
        specials = ['CREATE','SELECT','DELETE','INSERT']
        values = []
        try:
            values = query.split('(', 1)[1].split(')')[0].replace(',', '').split()
        except IndexError:
            # print("List don't consist brackets")
            values = query.replace(',', '').split()[2:]
        return values if specials not in values else [0]
        
        #//
        



if __name__ == '__main__':
    client = Parser()
    