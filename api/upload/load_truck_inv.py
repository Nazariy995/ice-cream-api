TR_NUM_S = 3
TR_NUM_L = 4
TR_NUM_E = TR_NUM_S + TR_NUM_L

ITEM_NUM_S = 0
ITEM_NUM_L = 4
ITEM_NUM_E = ITEM_NUM_S + ITEM_NUM_L

ADJUSTMENT_S = ITEM_NUM_E
ADJUSTMENT_L = 4
ADJUSTMENT_E = ADJUSTMENT_S + ADJUSTMENT_L

IR_NUM_S = 3
IR_NUM_L = 4
IR_NUM_E = IR_NUM_S + IR_NUM_L

FILENAME = "initial data/loadTruck.txt"

datas = []
with open(FILENAME, "r") as input:
    datas = input.readlines()

truck_inv = {"items":[]}
for data in datas[1:-1]:
    if "TR" in data:
        #Start of a new truck item load
        truck_inv = {}
        truck_inv["items"] = []
        truck_inv["truck_number"] = data[TR_NUM_S:TR_NUM_E]
    elif "IR" in data:
        #Update the inventory in the database
        truck_inv["IR"] = data[IR_NUM_S:IR_NUM_E]
        print truck_inv
    else:
        #Add item quantities
        db_item = {}
        db_item["item"] = data[ITEM_NUM_S:ITEM_NUM_E]
        db_item["quantity"] = data[ADJUSTMENT_S:ADJUSTMENT_E]
        truck_inv["items"].append(db_item)






