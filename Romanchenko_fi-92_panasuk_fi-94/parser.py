import storage, re

class Parser:

    def __init__(self):       
        query = ''                              #initial action for start of the application
        while not query.endswith(';'):
            query = query + ' ' + input('--> ')
        for command in query.split(';'):        #split commands with ';' : CREATE ...; SELECT ... 
            if command:                         # => in dif. commands
                self.action(command)
        
    def action(self, query:str) -> str:         #TODO: optimize this shit
        if query.split()[0].upper() == 'EXIT':
            action_call = self.exit()
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

    def exit(self) -> None:                         #qutting the application
        return quit()

    def error(self) -> None:                        #displaying error message
        return 'ERROR, COMMAND NOT FOUND'

    def parse_command(self, query) -> list:         #splits input for list of [command, column, values, *arg]
        regex = re.compile(r"\\n|\\t|\\r|/s|\W^\*") #regex for removing termination symbols
        query = re.sub(r"(?i)indexed",'INDEXED',regex.sub(" ",query))
        str = re.findall(r'\S+', query)
        
        command = str[0]

        columns = {}
        table_name = str[str.index(command)+1]      # if str[0] == CREATE => str[1] = table_name
        
        if command.upper() == 'CREATE':
            values = self.splitter(query)               #splitting query into arguments list
            try:
                if len(str) < 3: raise Exception('too short')
            except:
                print('The list is too short')
                return [0]

            for column in values:
                if column == 'INDEXED':
                    pass
                elif column == values[-1] or values[values.index(column)+1] != 'INDEXED':   
                    columns[column] = False
                elif values[values.index(column)+1] == 'INDEXED':
                    columns[column] = True

            return ['CREATE', table_name, columns]

        elif command.upper() == 'SELECT':
            selected = str[1]
            str = re.findall(r'\S+',re.sub(r"(?i)from",'FROM',query))

            table_name = str[str.index('FROM')+1]       
                
            return ['SELECT', table_name, selected]

        elif command.upper() == 'INSERT':
            values = self.splitter(query)
            table_name = str[1]

            return ['INSERT',table_name, values]

        elif command.upper() == 'DELETE':
            str = re.findall(r'\S+',re.sub(r"(?i)from",'FROM',query))
            try:
                table_name = str[str.index('FROM')+1]
            except ValueError:
                table_name = str[1]
            return ['DELETE', table_name]

    def splitter(self, query) -> list:
        #// CATCH input despite brackets
        specials = ['CREATE','SELECT','DELETE','INSERT']
        values = []
        try:
            values = query.split('(', 1)[1].split(')')[0].replace(',', ' ').replace("'",'').split()
        except IndexError:
            # print("List don't consist brackets")
            values = query.replace(',', ' ').split()[2:]
        return values if specials not in values else [0]
        #//
        

if __name__ == '__main__':
    client = Parser()
    