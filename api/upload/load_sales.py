from constants.truck_inventory import *
from constants.header import *
from datetime import datetime
from truck_inventory.models import TruckInventory
from truck_route.models import TruckRoute


class LoadSales:

    def load_truck_inventory(self, sales_file):
        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []

        date = self.load_date(truck_inventory_file[0])

        truck_inv = {"items":[]}
        TR_count = 0
        IR_count = 0
        for data in truck_inventory_file[1:-1]:
            if "TR" in data:
                IR_count = 0
                #Start of a new truck item load
                truck_inv = {}
                truck_inv["items"] = []
                truck_inv["truck_number"] = int(data[TR_NUM_S:TR_NUM_E])
                truck_inv["date"] = date
            elif "IR" in data:
                #End of truck assignment
                count = int(data[IR_NUM_S:IR_NUM_E])
                #Check if IR count is same
                errors["trailer"] += self.load_ir(count, IR_count, truck_inv["truck_number"])
                #Add items to the database
                errors["data"] += self.add_items(truck_inv)
                IR_count = 0
            else:
                TR_count += 1
                IR_count += 1
                #Add item quantities
                db_item = {}
                db_item["item_number"] = int(data[ITEM_NUM_S:ITEM_NUM_E])
                db_item["quantity"] = int(data[ADJUSTMENT_S:ADJUSTMENT_E])
                truck_inv["items"].append(db_item)

        errors["trailer"] += self.load_trailer(truck_inventory_file[-1], TR_count)

        return errors
