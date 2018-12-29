# Back End prototype for Queen's Intercity Excursion System
# Uses Transaction Summmary File from front end to update the output Valid Services File and New Central Services file
# Input File: OldCentralServicesFile.txt, MergedTransactionSummaryFile.txt
# Outpuf File: NewCentralServicesFile.txt, ValidServicesFile.txt

#IMPORTS
import sys

#GLOBAL VARIABLES
service_list = []
services = {}


#Writes Valid Services File based on transactions for output
def write_valid_services(filename):
    global services
    file_out = open(filename, 'w+')

    for k, v in services.items():
        file_out.write(str(k) + "\n")
    file_out.close()


#Writes Central Services File in order for output
def write_new_central_services(filename):
    global services
    file_out = open(filename, 'w+')

    # Sorts dictionary to be written out into the New Central Services File
    for key in sorted(services.keys()):
        file_out.write(key)
        for element in services[key]:
            file_out.write(' ' + str(element))
        file_out.write("\n")
    file_out.close()


# Changes ticket amount for 2 services
# Increases number of tickets for new service number
# Reduces number of tickets for old service number
def merge_change_ticket(line):
    global services
    old_service = services.get(line[1])
    new_service = services.get(line[3])
    old_ticket = int(old_service[1])
    new_ticket = int(new_service[1])
    change_ticket = int(line[2])

    # Checks if change of tickets will exceed capacity
    checkChange = old_ticket - change_ticket
    if (check_capacity_ticket(new_service[0], str(checkChange))):
        old_service[1] = old_ticket - change_ticket
        services[line[1]] = old_service
    else:
        print("Cannot change service due to capactiy and ticket number")

    # Checks if change of tickets will exceed capacity
    checkChange = new_ticket + change_ticket
    if (check_capacity_ticket(new_service[0], str(checkChange))):
        new_service[1] = new_ticket + change_ticket
        services[line[3]] = new_service
    else:
        print("Cannot change service due to capacity and ticket number")


# Cancels number of tickets for specific service number
# Looks up service number in dictionary to update ticket number
# Verifies ticket change remains within constraints
def merge_cancel_ticket(line):
    global services
    serviceLine = services.get(line[1])
    oldTick = int(serviceLine[1])
    canceledTick = int(line[2])
    newTick = oldTick - canceledTick

    if newTick > 0:
        serviceLine[1] = newTick
        services[line[1]] = serviceLine


# Updates ticket number for specific service number
# Looks up service number in dictionary to update ticket number
# Verifies ticket change remains within constraints
def merge_sell_ticket(line):
    global services
    serviceLine = services.get(line[1])
    oldTick = int(serviceLine[1])
    capacity = int(serviceLine[0])
    soldTickets = int(line[2])
    if soldTickets >= 1 and soldTickets <= capacity:
        oldTick += soldTickets
        check_capacity_ticket(str(capacity), str(oldTick))
        serviceLine[1] = oldTick
        services[line[1]] = serviceLine


# Deletes service
def merge_delete_service(line):
    global services
    del services[line[1]]


# Uses information from Transaction Summary File to add new service
# New service is added to dictionary
def new_create_service(line):
    global services
    # Assumes serivice capacity is 1000
    servCap = "1000"
    servName = line[4]
    servTick = line[2]
    servDate = line[5]
    if line[1] in services:
        print(line[1] + " invalid, cannot create new service")
    else:
        services[line[1]] = [servCap, servTick, servName, servDate]


# Uses each line of transaction summary file to execute services
def transaction_type(line):
    if line[0] == "CRE":
        new_create_service(line)
    elif line[0] == "DEL":
        merge_delete_service(line)
    elif line[0] == "SEL":
        merge_sell_ticket(line)
    elif line[0] == "CAN":
        merge_cancel_ticket(line)
    elif line[0] == "CHG":
        merge_change_ticket(line)
    else:
        print("Back End Complete")


# Converts line of transaction summary file into an array
def split_transactions(item):
    splitLine = item.split()
    if len(splitLine) < 6:
        print("Invalid transaction summary File")

    else:
        # if service name contains the ' ' character this condenses it into a 6 element array
        if len(splitLine) >= 6:
            splitLine[4:-1] = [''.join(splitLine[4:-1])]
            return splitLine


# Reads transaction summary file
# Splits each line into an array for analysis
def read_transaction_file(filename):
    global services
    filein = open(filename, 'r')
    transactions = filein.read().splitlines()
    filein.close()

    for item in transactions:
        splitLine = split_transactions(item)
        transaction_type(splitLine)


# Validates date meets constraints
def check_date(date):
    if len(date) == 8:
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:8])
        if year in range(1980, 2999) and month in range(1, 12) and day in range(1, 31):
            return True
    print("Invalid date")
    return False


# Validates service name meets contstraints
def check_service_name(servName):
    if 3 <= len(servName) <= 39:
        if all([x.isalnum() or x == ' ' for x in servName]):
            if servName.startswith(' ') or servName.endswith(' '):
                print("Invalid service name")
                return False
            else:
                return True
    return False


# Validates ticket number and capactity meets constraints
# Validates ticket number is not greater than capacity
def check_capacity_ticket(servCap, tickNum):
    if servCap.isdigit() and 1 <= int(servCap) <= 1000:
        if tickNum.isdigit() and 1 <= int(tickNum) <= 1000:
            if int(servCap) >= int(tickNum):
                return True
    print("Invalid service capacity and ticket number")
    return False


# Validates service number meets constraints
def check_service_num(servNum):
    if servNum.isdigit() and len(servNum) == 5 and not servNum.startswith('0'):
        return True
    else:
        print("Invalid service number in Central Services File")
        return False


# Each line in the Central Services File is split into AAAA CCCC MMM NNNN format
# Each line verified to meet constraints
# Each service is stored in a dictionary by their service number for easy access
def split_services_file(line):
    global services
    splitLine = line.split()
    if len(splitLine) < 5:
        print("Invalid Central Services File")

    else:
        if len(splitLine) > 5:
            splitLine[3:-1] = [''.join(splitLine[3:-1])]
        check_service_num(splitLine[0])
        check_capacity_ticket(splitLine[1], splitLine[2])
        check_service_name(splitLine[3])
        check_date(splitLine[4])
        services[splitLine[0]] = splitLine[1:]


# Reads in Old Central Services File
# Validates each line by calling split_services_file
def read_central_services_file(filename):
    global service_list
    filein = open(filename, 'r')
    service_list = filein.read().splitlines()
    filein.close()

    # Validates length
    # If valid it will input information into array
    lines = len(service_list)
    for item in service_list:
        length = len(item)
        if length - 1 > 63:
            print("Invalid Central Services File")
        else:
            split_services_file(item)


def main():
    # Turn arguments into input and output files
    args = sys.argv
    old_CentralServicesFile = args[1]
    mergedTransactionFile = args[2]
    new_CentralServicesFile = args[3]
    validServicesFile = args[4]

    # Reads input files and writes output files
    read_central_services_file(old_CentralServicesFile)
    read_transaction_file(mergedTransactionFile)
    write_new_central_services(new_CentralServicesFile)
    write_valid_services(validServicesFile)

main()
