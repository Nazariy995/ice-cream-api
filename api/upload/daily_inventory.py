#Item Number boundries
ITEM_NUM_S = 0
ITEM_NUM_L = 4
ITEM_NUM_E = ITEM_NUM_S + ITEM_NUM_L
#Warehouse Quantiry Boundries
WAREHOUSE_Q_S = ITEM_NUM_E
WAREHOUSE_Q_L = 6
WAREHOUSE_Q_E = WAREHOUSE_Q_S + WAREHOUSE_Q_L
#Price Boundries
PRICE_S = WAREHOUSE_Q_E
PRICE_L = 4
PRICE_E = PRICE_S + PRICE_L
#Description Boundries
DESCR_S = PRICE_E
DESCR_L = 30
DESCR_E = DESCR_S + DESCR_L

FILENAME = "initial data/dailyInventory.txt"
datas = []
with open(FILENAME, "r") as input:
    datas = input.readlines()
    

#start from position 1 because the first position is the header
#we end with position -1 becuase we don't want the trailer record
for data in datas[1:-1]:
    db_data = {}
    db_data["item_number"] = data[ITEM_NUM_S:ITEM_NUM_E]
    db_data["quantity"] = data[WAREHOUdSE_Q_S:WAREHOUSE_Q_E]
    db_data["price"] = data[PRICE_S:PRICE_E]
    db_data["description"] = data[DESCR_S:DESCR_E].strip()
    print db_data


