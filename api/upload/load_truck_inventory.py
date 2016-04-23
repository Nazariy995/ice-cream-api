from constants.truck_inventory import *

class LoadTruckInventory:

    def load_truck_inventory(self, truck_inventory_file):
        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []

        date = self.load_date(truck_inventory_file[0])

        truck_inv = {"items":[]}
        TR_count = 0
        for data in truck_inventory_file[1:-1]:
            if "TR" in data:
                IR_count = 0
                #Start of a new truck item load
                truck_inv = {}
                truck_inv["items"] = []
                truck_inv["truck_number"] = data[TR_NUM_S:TR_NUM_E]
                truck_inv["date"] = date
            elif "IR" in data:
                #Update the inventory in the database
                count = data[IR_NUM_S:IR_NUM_E]
                errors["trailer"] += self.load_ir(count, IR_count, truck_inv["truck_number"])
                IR_count = 0
            else:
                TR_count += 1
                IR_count += 1
                #Add item quantities
                db_item = {}
                db_item["item"] = data[ITEM_NUM_S:ITEM_NUM_E]
                db_item["quantity"] = data[ADJUSTMENT_S:ADJUSTMENT_E]
                truck_inv["items"].append(db_item)




    def add_items(self, truck_inv):
        print truck_inv

    def load_ir(self, trailer, trailer_check_count, truck_number):
        errors = []
        try:
            #Check if the trailer count matches
            if trailer_check_count != trailer_count:
                raise ValueError("Trailer count does not match. Please Fix it in the file.")

        except ValueError as err:
            errors.append(str(err))

        return errors

    def load_date(self, header):
        date = header[DATE_START:DATE_END]
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        return date_object








