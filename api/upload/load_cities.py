# needed for regex:
import re
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



# open for reading
file = open('sample.txt','r')
# open for writing
output = open('cities.txt', 'w')

# Populate lines[] with the lines of the file
lines = [] # start with empty list
for line in file.readlines() :
    lines.append(line)
    
    
# Extract the header and date
header = lines[0]
del lines[0]
output.write(header[3:7])
output.write('\n')
#print "Header: "+header


#date
date = header[DATE_START:DATE_END]
date_object = datetime.strptime(date, '%Y-%m-%d').date()
print date_object

# Extract the trailer
trailer = int(lines.pop()[2:])

#print "Trailer: "+trailer


# Remaining lines
listified = []
for line in lines :
    finds = list(re.search('(.{20})(.{20})(.{2})',line).groups())
    
    for i in range(len(finds)) :
        finds[i] = finds[i].strip()

    listified.append(finds)

# YAY
count = 0;
for entity in listified : 
    #print entity
    output.write(','.join(entity))
    output.write('\n')
    count+=1
    
#output.write(trailer) check if # records matches trailer
if count != trailer:
    print 'error!'

output.close()
file.close()
    