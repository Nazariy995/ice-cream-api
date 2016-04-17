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

daily_inventory = []
with open("dailyInventory.txt", "r") as input:
    daily_inventory = input.readlines()
    

#start from position 1 because the first position is the header
#we end with position -1 becuase we don't want the trailer record
for item in daily_inventory[1:-1]:
    db_item = {}
    db_item["item_number"] = item[ITEM_NUM_S:ITEM_NUM_E]
    db_item["quantity"] = item[WAREHOUSE_Q_S:WAREHOUSE_Q_E]
    db_item["price"] = item[PRICE_S:PRICE_E]
    db_item["description"] = item[DESCR_S:DESCR_E].strip()
    print db_item
    
    