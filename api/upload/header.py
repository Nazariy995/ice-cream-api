from datetime import datetime

#Header Name Boundries
SPACE = 1
HEADER_NAME_START = 0
HEADER_NAME_LEN = 2
HEADER_NAME_END = HEADER_NAME_START + HEADER_NAME_LEN
#Sequence Number Boundries
SEQUENCE_START = HEADER_NAME_END + SPACE
SEQUENCE_LEN = 4
SEQUENCE_END = SEQUENCE_START + SEQUENCE_LEN
#Date Boundries
DATE_START = SEQUENCE_END + (6 * SPACE)
DATE_LEN = 10
DATE_END = DATE_START + DATE_LEN

FILENAME = "dailyInventory.txt"

with open(FILENAME, "r") as input:
    daily_inventory = input.readlines()
    
header = daily_inventory[0]
header_name = header[HEADER_NAME_START:HEADER_NAME_END]
#Check if header name is HD
sequence_number = header[SEQUENCE_START:SEQUENCE_END]
#Check if the sequence number is greater then the last sequence number
date = header[DATE_START:DATE_END]
#Check if the date is equal or greater then the last uploaded data
#Check if the date fits the format
date_object = datetime.strptime(date, '%Y-%m-%d').date()
print date_object


