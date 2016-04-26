from constants.truck_inventory import *
from constants.header import *
from datetime import datetime
from datetime import date as current_date
from warehouse_inventory.models import WarehouseInventory
from truck_inventory.models import TruckInventory
from default_inventory.models import DefaultInventory
from trucks.models import Truck
import logging
log = logging.getLogger('ice_cream_api')


class LoadTruckInventory:

    def load_truck_inventory(self, truck_inventory_file):
        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []

        date = self.load_date(truck_inventory_file[0])
#        today = datetime.now(eastern).date()
        #Check if the date matches today
#        if today != date:
#            errors["date"].append("The date on the file does not match today's date. Please fix it!")
#            return errors
        print date
        self.set_default_truck_inventory(date)


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

        log.info("Truck Inventory has been updated")

        return errors

    def add_items(self, truck_inv):
        errors = []
        truck_number = truck_inv["truck_number"]
        date = truck_inv["date"]
        try:
            for new_item in truck_inv["items"]:
                #Get all the assigned items for this truck for the specific date
                truck_inventory = TruckInventory.objects.filter(truck_number=truck_number)
                #Get the count of truck inventory
                count = truck_inventory.count()
                #Get the item from the warehouse inventory
                db_item = WarehouseInventory.objects.filter(item_number=new_item["item_number"]).first()
                #If it is not in the warehouse inventory then make an error and continue on to the next item
                if not db_item:
                    error = "Item number {} not in the warehouse inventory".format(new_item["item_number"])
                    errors.append(error)
                    log.error(error)
                    continue
#                #Get the specifica item in the truck inventory
                truck_inventory_item = truck_inventory.filter(item_number=new_item["item_number"]).first()
                #if it exists then update the new inventory
                if truck_inventory_item:
                    adjustment = new_item["quantity"]
                    #Apply adjustments to the current quantity
                    new_quantity = truck_inventory_item.quantity + adjustment
                    #if new quantity is greater then 0 proceed
                    if new_quantity >= 0:
                        #Check if the new adjustment exceeeds the current warehouse inventory
                        if adjustment > db_item.quantity:
                            #assign whatever is in the warehouse inventory
                            adjustment = db_item.quantity
                            #new warehouse inventory = 0
                            db_item.quantity = 0
                        else:
                            #subtract from warehouse inventory
                            db_item.quantity -= adjustment

                        truck_inventory_item.quantity += adjustment
                        #Update both the warehouse inventory and the  truck inventory
                        db_item.save()
                        truck_inventory_item.save()
                    else:
                        error = "New inventory amount for truck {} and item {} is negative".format(truck_number, new_item["item_number"])
                        log.error(error)
                        errors.append(error)
                else:
                    #include the count for the current item that we are about to add
                    count += 1
                    #if count is greater then max of 10 then we raise an exception
                    if count > MAX_ITEMS:
                        raise Exception("Items exceeded for truck number {}".format(truck_number))
                    #Add new truck inventory item to the databases
                    db_truck_inv = {}
                    db_truck_inv["date_added"] = date
                    db_truck_inv["truck_number"]= truck_number
                    db_truck_inv["item_number"] = new_item["item_number"]
                    quantity = new_item["quantity"]
                    if quantity < 0:
                        error = "New inventory amount for truck {} and item {} is negative".format(truck_number, new_item["item_number"])
                        log.error(error)
                        errors.append(error)
                        continue
                    #if the quantity exceed the current warehouse inventory then assign whatever we have
                    if quantity > db_item.quantity:
                        quantity = db_item.quantity
                        db_item.quantity = 0
                    else:
                        db_item.quantity -= quantity
                    db_item.save()
                    db_truck_inv["quantity"] = quantity
                    db_truck_inv["price"] = db_item.price
                    db_truck_inv["description"] = db_item.description
                    #Save the new truck inventory to the database
                    created = TruckInventory.objects.create(**db_truck_inv)
        except Exception as e:
            error = str(e)
            log.error(error)
            errors.append(error)

        return errors

    def load_ir(self, trailer_count, trailer_check_count, truck_number):
        errors = []
        try:
            #Check if the trailer count matches
            if trailer_check_count != trailer_count:
                raise ValueError("IR count for truck {} does not match. Please Fix it in the file.".format(truck_number))

        except ValueError as err:
            log.error(str(err))
            errors.append(str(err))

        return errors

    def load_trailer(self, trailer, trailer_check_count):
        from constants.trailer import *
        errors = []
        try:
            #Convert trailer count to a number
            trailer_count = int(trailer[TR_NUM_S:TR_NUM_E])
            #Check if the trailer count match
            if trailer_check_count != trailer_count:
                raise ValueError("Trailer count does not match. Please Fix it in the file.")
        except ValueError as err:
            log.error(str(err))
            errors.append(str(err))
        return errors

    def load_date(self, header):
        date = header[DATE_START:DATE_END]
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        return date_object

    #Set the Default Inventory at the start of each day
    def set_default_truck_inventory(self, date):
        errors = []
        default = DefaultInventory.objects.all()
        trucks = Truck.objects.all()
        for truck in trucks:
            truck_number = truck.truck_number
            for item in default:
                db_truck_inventory = {}
                db_truck_inventory["truck_number"] = truck_number
                db_truck_inventory["item_number"] = item.item_number
                #Check if the item is in the warehouse inventory
                try:
                    db_item = WarehouseInventory.objects.get(item_number=item.item_number)
                except:
                    error = "Default inventory item {} not in the warehouse inventory".format(item.item_number)
                    errors.append(error)
                    log.error(error)
                    continue
                #Save the price for later use
                db_truck_inventory["price"] = db_item.price
                db_truck_inventory["description"] = db_item.description
                #If quantity is greater then the warehouse inventory then assign what is left over
                if item.quantity > db_item.quantity:
                    quantity = db_item.quantity
                    db_item.quantity = 0
                else:
                    quantity = item.quantity
                    db_item.quantity -= quantity
                db_item.save()
                db_truck_inventory["quantity"] = quantity
                db_truck_inventory["date_added"] = date
                db_truck_inv = TruckInventory.objects.create(**db_truck_inventory)

        return errors

