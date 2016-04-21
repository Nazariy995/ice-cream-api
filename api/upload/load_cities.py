# needed for regex:
import re
from datetime import datetime

FILENAME = "initial data/cityUpload.txt"

# open for reading
file = open(FILENAME,'r')

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


# Populate lines[] with the lines of the file
lines = [] # start with empty list
for line in file.readlines() :
    lines.append(line)
    
    
# Extract the header
header = lines[0]
del lines[0]
#print "Header: "+header


# Extract the trailer
trailer = lines.pop()
#trailer = int(trailer[2:])
#print trailer

#date
date = header[DATE_START:DATE_END]
date_object = datetime.strptime(date, '%Y-%m-%d').date()
#print date_object


# Remaining lines
listified = []
for line in lines :
    finds = list(re.search('(.{20})(.{20})(.{2})',line).groups())
    
    for i in range(len(finds)) :
        finds[i] = finds[i].strip()

    listified.append(finds)

# YAY
count = 0
for entity in listified : 
    listified[count].append(date_object)
    count+=1
    print entity
    
#Check to see if trailer record is accurate
# if count != trailer:
#     print "Number of records does not match the trailer record!!!"