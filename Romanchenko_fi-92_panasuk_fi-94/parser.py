import storage as db, re
storage = db.db()
class Parser:

    NAMES = r"[a-zA-Z]+|\d+" 
    COMMANDS = ["CREATE", "INSERT", "SELECT", "DELETE"]
    SPECIAL_WORDS = ["INDEXED", "INTO", "FROM", "WHERE"]
    OPERATORS = ["=", "!=", ">", "<", ">=", "<="]

    def __init__(self):       
        query = ''                              #initial action for start of the application
        while True:
            query += ' ' + input(">").strip()
            if ';' in query:
                for command in query.split(';'): # Split commands with ';' : CREATE ...; SELECT ...
                    if command:
                        command = command.strip()
                        if command.upper() == 'EXIT': # Exit command to stop the program
                            raise self.exit()
                        try:
                            response = self.action(command) # Try to parse and complete the commands
                        except IndexError:
                            response = self.error()
                        # except Exception as error:
                        #     response = 'Error: {}'.format(str(error))
                        print(response)
                        
                        query = ''
        #create cast (id indexed, name, value); insert cast (1, alex, meow); select * from cast;
        #create cast (id indexed, name, value); insert cast (1, alex, meow); select name from cast;
        #create cast (id indexed, name, value); insert cast (1, alex, meow); select name from cast; delete from cast; select * from cast;
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
            action_call = storage.select(table_name, columns, condition = [])
        elif command == 'INSERT':
            _, table_name, values = query
            action_call = storage.insert(table_name, values)
        elif command == 'DELETE':
            _, table_name = query
            action_call = storage.delete(table_name, condition = [])
        else:
            action_call = self.error()

        return action_call

    def exit(self) -> None:                         #qutting the application
        return quit()



    def parse_command(self, query) -> list:         #splits input for list of [command, column, values, *arg]
        regex = re.compile(r"\\n|\\t|\\r|/s|\W^\*") #regex for removing termination symbols
        query = re.sub(r"[\(,\)]", " ",re.sub(r"(?i)indexed",'INDEXED',regex.sub(" ",query)))
        expression = re.findall(r'\S+', query)
        indexation = 0
        columns = {}
        if re.match(r"(?i)create", query):
            table_name = expression[1]
            for column in expression[2:]:
                if column == 'INDEXED':
                    pass
                elif column == expression[-1] or expression[expression.index(column)+1] != 'INDEXED':   
                    columns[column] = False
                elif expression[expression.index(column)+1] == 'INDEXED':
                    columns[column] = True
                    indexation +=1
            if indexation in [0,1]:
                return ['CREATE',table_name, columns]

        elif re.match(r"(?i)select", query):

            expression = re.findall(r'\S+',re.sub(r"(?i)from",'FROM',query))

            table_name = expression[expression.index('FROM')+1]     
            selected = expression[1:expression.index('FROM')]
            return ['SELECT', table_name, selected]

        elif re.match(r"(?i)insert", query):
            values = []
            try:
                expression = re.findall(r'\S+',re.sub(r"(?i)into",'INTO',query))
                into = expression.index('INTO')+1
                table_name = expression[into]

                for i in expression[into+1:]:
                    if i.upper() in self.SPECIAL_WORDS:
                        pass
                    elif re.match(self.NAMES, i):
                        values.append(i)
            except Exception:
                table_name = expression[1]
                for i in expression[2:]:
                    if i.upper() in self.SPECIAL_WORDS:
                        pass
                    elif re.match(self.NAMES, i) and i.upper() not in self.SPECIAL_WORDS:
                        values.append(i)
            return ['INSERT', table_name, values]


        elif re.match(r"(?i)delete", query):
            expression = re.findall(r'\S+',re.sub(r"(?i)from",'FROM',query))
            try:
                table_name = expression[expression.index('FROM')+1]
            except ValueError:
                table_name = expression[1]
            return ['DELETE', table_name]


if __name__ == '__main__':
    client = Parser()
    