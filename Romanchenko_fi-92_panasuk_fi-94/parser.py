import storage as db, re
storage = db.db()
class Parser:

    NAMES = r"[a-zA-Z][a-zA-Z0-9_]*"
    COMMANDS = {"CREATE", "INSERT", "SELECT", "DELETE"}
    SPECIAL_WORDS = {"INDEXED", "INTO", "FROM", "WHERE",}
    OPERATORS = {"=", "!=", ">", "<", ">=", "<="}
    OPERATORS_LIST = list(OPERATORS)


    def __init__(self):       
        query = ''                              #initial action for start of the application
        while True:
            query += " " + input("-->").strip()
            if ";" in query:
                for command in query.split(";"): # Split commands with ';' : CREATE ...; SELECT ...
                    if command:
                        command = command.strip()
                        if command.upper() == "EXIT": # Exit command to stop the program
                            raise Parser.StopTheLoop
                        try:
                            response = self.action(command) # Try to parse and complete the commands
                        except IndexError:
                            response = "ERROR: invalid command! Try again."
                        except Exception as e:
                            response = "ERROR: {}".format(str(e))
                        print(response)
                        query = ""
        
    def action(self, query:str) -> str:         #TODO: optimize this shit
        if query.split()[0].upper() == 'EXIT':
            action_call = self.exit()
        query = self.parse_command(query)       #split input command to the list with needed arguments
        command = query[0]
        

        if command == 'CREATE':
            _, table_name, columns = query
            action_call = storage.create(table_name, columns)
        elif command == 'SELECT':
            _, table_name, columns, condition = query
            action_call = storage.select(table_name, columns, condition)
        elif command == 'INSERT':
            _, table_name, values = query
            action_call = storage.insert(table_name, values)
        elif command == 'DELETE':
            _, table_name, condition = query
            action_call = storage.delete(table_name, condition)
        else:
            action_call = self.error()

        return action_call

    def exit(self) -> None:                         #qutting the application
        return quit()

    def error(self) -> None:                        #displaying error message
        return 'ERROR, COMMAND NOT FOUND'

    def parse_command(self, query) -> list:         #splits input for list of [command, column, values, *arg]
        query = query.split()
        query = list(filter(lambda x: x != "", sum([elements.split(",") for elements in query], [])))
        command = query[0]
        for i, element in enumerate(query):
            if element not in Parser.OPERATORS_LIST:
                check = [operator in element for operator in Parser.OPERATORS_LIST]
                if any(check):
                    operator = Parser.OPERATORS_LIST[check.index(True)]
                    insert_element = element.split(operator)
                    insert_element.insert(1, operator)
                    query = query[:i] + insert_element + query[i + 1]
                    break
        str = []
        i = 0

        while i < len(query) and query[i].upper() not in Parser.COMMANDS: 
            i += 1
        if i >= len(query):
            raise Exception("command not found!")

        command_type = query[i].upper()
        str.append(command_type)
        i += 1
        
        columns =[]

        if command.upper() == 'CREATE':
            if re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                str.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name!")

            columns = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                if re.match(Parser.NAMES, query[i]):
                    if query[i].upper() in Parser.SPECIAL_WORDS:
                        raise Exception("special word before column name!")
                    if (i + 1) < len(query):
                        next_element = query[i + 1]
                        for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                            if symbols in next_element:
                                next_element = next_element.replace(symbols, "")
                        isIndexed = next_element.upper() == "INDEXED"
                    else:
                        isIndexed = False
                    columns.append([query[i], isIndexed])
                    i += isIndexed
                i += 1

            str.append(columns)


        elif command.upper() == 'SELECT':
            columns = []

            while i < len(query) and query[i].upper() != "FROM":
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                if query[i] == "*":
                    columns = []
                    i += 1
                elif re.match(Parser.NAMES, query[i]) and query[i].upper() not in Parser.SPECIAL_WORDS:
                    columns.append(query[i])
                    i += 1
                else:
                    raise Exception("invalid column name!")

            if i < len(query) and query[i].upper() == "FROM":
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")

                str.append(query[i])
                str.append(columns)
                i += 1  
            else:
                raise Exception("invalid table name!")

            condition = []

            if i < len(query) and query[i].upper() == "WHERE":
                i += 1
                while i < len(query) and len(condition < 3):
                    for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                        if symbols in query[i]:
                            query[i] = query[i].replace(symbols, "")
                    condition.append(str(query[i]))
                    i += 1
            str.append(condition)


        elif command.upper() == 'INSERT':
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                str.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name!")

            values = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                values.append(query[i])
                i += 1
                

            str.append(values)


        elif command.upper() == 'DELETE':
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1
            if i < len(query) and re.match(Parser.NAMES, query[i]) and not query[i].upper() in Parser.SPECIAL_WORDS:
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                str.append(query[i])
                i += 1
            else:
                raise Exception("invalid table name")
            if i < len(query) and query[i].upper() in Parser.SPECIAL_WORDS:
                i += 1

            condition = []

            while i < len(query):
                for symbols in ["(", ")", ",", ";", "\t", "\n", "\r"]:
                    if symbols in query[i]:
                        query[i] = query[i].replace(symbols, "")
                condition.append(str(query[i]))
                if query[i].upper() in Parser.SPECIAL_WORDS:
                    raise Exception("invalid column name in WHERE!")
                condition.append(query[i])
                i += 1
            str.append(condition)

        return str


if __name__ == '__main__':
    client = Parser()
    