#Truck  Number Boundries
TRUCK_NUM_S = 0
TRUCK_NUM_L = 4
TRUCK_NUM_E = TRUCK_NUM_S + TRUCK_NUM_L
#Route Number Boundries
ROUTE_NUM_S = TRUCK_NUM_E
ROUTE_NUM_L = 4
ROUTE_NUM_E = ROUTE_NUM_S + ROUTE_NUM_L

FILENAME = "initial data/truckRouteUpload.txt"
datas = []
with open(FILENAME, "r") as input:
    datas = input.readlines()

for data in datas[1:-1]:
    db_data = {}
    db_data["truck"] = data[TRUCK_NUM_S:TRUCK_NUM_E]
    db_data["route"] = data[ROUTE_NUM_S:ROUTE_NUM_E]
    print db_data
