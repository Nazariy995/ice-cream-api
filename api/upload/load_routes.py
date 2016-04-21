
FILENAME = "initial data/routeUpload.txt"
MAX_CITIES = 10
#Action Boundry
ACTION_S = 0
ACTION_L = 1
ACTION_E = ACTION_S + ACTION_L
#Route Number Boundry
ROUTE_N_S = ACTION_E
ROUTE_N_L = 4
ROUTE_N_E = ROUTE_N_S + ROUTE_N_L
#Cities Boundry
CITIES_S = ROUTE_N_E
CITIES_L = 20
CITIES_E = None


# Populate lines[] with the lines of the file
lines = [] # start with empty list
with open(FILENAME,'r') as input:
    lines = input.readlines()

# Remaining lines
listified = []
for line in lines[1:-1]:
    route = {}
    action = line[ACTION_S:ACTION_E]
    route_number = line[ROUTE_N_S:ROUTE_N_E]
    city_labels = line[CITIES_S:CITIES_E]
    cities = []
    city_start_location = CITIES_S
    while city_start_location < len(line):
        city_end_location = city_start_location + CITIES_L
        city = line[city_start_location:city_end_location].strip()
        cities.append(city)
        city_start_location = city_end_location
    #If number of cities exceeds 10 return error
    #Action = C Delete all the Foreign keys and replace the cities with the new one
    #ACtion = C error if city labal not in repository.

