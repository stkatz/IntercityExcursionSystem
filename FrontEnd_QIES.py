#Front End Prototype for Queen's Intercity Excursion Program
#Allows a planner or agent to login to complete transactions based on user input

service_list = []
currentService = []
transactionFile = []
cancels = 0


# Checks if service name raw_input by user meets requirements
def check_service_name(service_name):
    if 3 <= len(service_name) <= 39:
        if all([x.isalnum() or x == ' ' for x in service_name]):
            if service_name.startswith(' ') or service_name.endswith(' '):
                return False
            else:
                return True
    return False


def check_service_num():
    global service_list
    print("Please enter existing service number: ")
    while True:
        service_num = input("")
        if service_num in service_list:
            print("Invalid, please enter new service number")
        else:
            break
    return service_num


# Creates transaction message for services completed
# Appended to a list to later be written into the output file
def make_line(serv, num1, tick, num2, name, date):
    global transactionFile
    line = serv + " " + num1 + " " + tick + " " + num2 + " " + name + " " + date
    transactionFile.append(line)

    
def write_transaction_summary():
    global transactionFile
    #Writes transaction messages to file
    fileout = open("TransactionSummaryFile.txt", '+w')
    for line in transactionFile:

        fileout.write(line)
        fileout.write("\n")
    fileout.write("EOS 00000 0 00000 **** 0")
    fileout.close()


#Completes logout, write transfaction summary file
def logout():
    invalid = True
    #Writes output file
    write_transaction_summary()
    #Only allows login after logout
    print("To begin a new session 'login': ")
    while invalid:
        newSession = input("")
        if newSession == "login":
            login()
            invalid = False
        elif newSession == "exit":
            break
        else:
            "Invalid command, please 'login': "

            
# Completes deleteservice transaction, validates raw_inputs
def delete_service():
    invalid = True
    global service_list
    # Validates raw_input service number exists in raw_input file
    service_num = check_service_num()
    print("Please enter service name: ")
    while invalid:
        service_name = input("")
        correct = check_service_name(service_name)
        if correct:
            service_list.remove(service_num)
            invalid = False
        else:
            continue
    make_line("DEL", service_num, "0", "00000", service_name, "0")


# Completes createservice transaction, validates raw_inputs from user
def create_service():
    global currentServices
    global service_list
    serv_num_valid = True
    date_valid = True
    serv_name_valid = True
    # Validates raw_input service number
    print("Please enter new service number: ")
    while serv_num_valid:
        service_num = input("")
        if service_num.isdigit():
            if len(service_num) != 5 or service_num.startswith('0') or service_num in service_list:
                print("Invalid service number, please try again: ")
                continue
            else:
                serv_num_valid = False
        else:
            print("Invalid service number, please try again: ")

    # validates raw_input date
    print("Please enter date: ")
    while date_valid:
        date = input("")
        try:
            int(date)
        except ValueError:
            print("Invalid date, please try again: ")
            continue
        if len(date) == 8:
            year = int(date[0:4])
            month = int(date[4:6])
            day = int(date[6:8])
            if year in range(1980, 2999) and month in range(1, 12) and day in range(1, 31):
                date_valid = False
            else:
                print("Invalid date, please try again: ")
                continue
        else:
            print("Invalid date, please try again: ")
            continue
    # validates service name
    print("Please enter service name: ")
    while serv_name_valid:
        service_name = input("")
        correct = check_service_name(service_name)
        if correct:
            serv_name_valid = False
        else:
            print("Invalid service name, please try again: ")
            continue
    make_line("CRE", service_num, "0", "00000", service_name, date)

    
# Completes changeticket transaction, validates raw_inputs
# Different requirements based on uer
def changeticket(user):
    global changes
    global service_list
    invalid = True
    # Validates service number exists in raw_input file

    old_service = check_service_num()
    print("Please enter existing service number: ")
    while invalid:
        new_service = input("")
        if new_service in service_list:
            # Validates raw_input number of tickets based on user or planner
            print("Please enter the number of tickets: ")
            while invalid:
                try:
                    ticket_num = int(input(""))
                except ValueError:
                    print("Invalid ticket number, please try again: ")
                    continue
                else:
                    if user == "planner" and 1 <= int(ticket_num) <= 1000:
                        invalid = False
                    elif user == "agent" and changes < 20:
                        if ticket_num + changes > 20:
                            print("Cannot change this many tickets ", 20 - changes,
                                  " remaining changeable tickets")
                            print("Please try again: ")
                        else:
                            changes += ticket_num
                            print("correct ", changes)
                            x = False
                    else:
                        print("Invalid ticket number, please try again: ")
        else:
            print("Invalid service number, please try again: ")

    make_line("CHG", old_service, str(ticket_num), new_service, "****", "0")


# Completes canceltickets transaction, validates raw_inputs
def cancel_ticket(user):
    global cancels
    global service_list
    invalid = True
    # Validates service number exists in raw_input file
    service_num = check_service_num()
    print("Please enter the number of tickets: ")
    while invalid:
        try:
            ticket_num = int(input(""))
        except ValueError:
            print("Invalid ticket number, please try again: ")
            continue
        else:
            if user == "agent":
                if 1 <= ticket_num <= 10 and cancels <= 20:
                    cancels += ticket_num
                    if (cancels > 20):
                        print("Exceeded, cancellation with this transaction", cancels)
                        cancels -= ticket_num
                    else:
                        invalid = False
                else:
                    print("Exceeded cancellation limit", cancels)
                    invalid = False
            elif user == "planner":
                if 1 <= ticket_num <= 1000:
                    invalid = False
                else:
                    print("Invalid ticket number, try again: ")
            else:
                print("Invalid ticket number, please try again: ")

    make_line("CAN", service_num, str(ticket_num), "00000", "****", "0")


# Completes sellticket transaction, validates raw_inputs
def sell_ticket():
    global service_list
    invalid = True
    # Validates service number exists in raw_input file
    service_num = check_service_num()
    print("Please enter the number of tickets: ")
    while invalid:
        try:
            ticket_num = int(input(""))
        except ValueError:
            print("Invalid ticket number, please try again: ")
            continue
        else:
            if 1 <= int(ticket_num) <= 1000:
                invalid = False
            else:
                print("Invalid ticket number, please try again: ")

    make_line("SEL", service_num, str(ticket_num), "00000", "****", "0")


#Allows accepted transactions based on user type
#Directs to service based on input
def transactions(user):
    while True:
        print("Enter Transaction: ")
        transaction = input("")
        if transaction == "sellticket":
            sell_ticket()
        elif transaction == "cancelticket":
            cancel_ticket(user)
        elif transaction == "changeticket":
            changeticket(user)
        elif transaction == "createservice" and user == "planner":
            create_service()
        elif transaction == "deleteservice" and user == "planner":
            delete_service()
        elif transaction == "logout":
            logout()
            break
        else:
            print("Invalid transaction, please try again.")


#Validates input Valid Services List File based on requirements
def check_valid_services_list(filename):
    global service_list
    #reads in file
    file_in = open(filename, 'r')
    service_list = file_in.read().splitlines()
    file_in.close()

    length = len(service_list) -1
    for item in service_list[0:length]:
        #item is 5 chracters, a digit and does not start with 0
        if len(item) != 5 or not item.isdigit() or item.startswith('0'):
            print("Valid Services List File is invalid")
            exit()
    #Last line is 00000
    if service_list[-1] != "00000":
        print("Valid Services List File is invalid")
        exit()


#Completes login, allows user to input planner or agent then validates input file
def login():
    print("Login as planner or agent: ")
    while True:
        user_type = input("")
        if user_type == "agent" or user_type == "planner":
            transactions(user_type)
            break
        else:
            print("Invalid command, please try again!")


#Prompts user to being sessions by logging in
def main():
    print("Welcome, please 'login' to begin: ")
    while True:
        user_login = input("")
        if user_login == "login":
            check_valid_services_list("ValidServicesList.txt")
            login()
            break
        else:
            print("Invalid command, please try again")
main()
