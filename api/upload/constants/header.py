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
