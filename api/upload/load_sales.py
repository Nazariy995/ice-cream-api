from constants.sales import *
from constants.header import *
from datetime import datetime
from truck_inventory.models import TruckInventory
from truck_route.models import TruckRoute


class LoadSales:

    def load_sales(self, sales_file):
        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []

        date = self.load_date(sales_file[0])

        truck_sales = {"items":[]}
        TR_count = 0
        SR_count = 0
        for data in sales_file[1:-1]:
            if "TR" in data:
                SR_count = 0
                #Start of a new truck item load
                truck_sales = {}
                truck_sales["items"] = []
                truck_sales["truck_number"] = int(data[TR_NUM_S:TR_NUM_E])
                truck_sales["date"] = date
            elif "SR" in data:
                #End of truck assignment
                count = int(data[SR_NUM_S:SR_NUM_E])
                #Check if SR count is same
                errors["trailer"] += self.load_sr(count, SR_count, truck_sales["truck_number"])
                #Add items to the database
                print truck_sales
#                errors["data"] += self.add_items(truck_sales)
                SR_count = 0
            else:
                TR_count += 1
                SR_count += 1
                #Add item quantities
                db_item = {}
                db_item["item_number"] = int(data[ITEM_NUM_S:ITEM_NUM_E])
                db_item["quantity"] = int(data[FINAL_Q_S:FINAL_Q_E])
                truck_sales["items"].append(db_item)

        errors["trailer"] += self.load_trailer(sales_file[-1], TR_count)

        return errors

#    def add_items(self, truck_sales):
#        errors = []
#        truck_number = truck_sales["truck_number"]
#        date = truck_sales["date"]
#        try:
#            for item_sale in truck_inv["items"]:

    def load_sr(self, trailer_count, trailer_check_count, truck_number):
        errors = []
        try:
            #Check if the trailer count matches
            if trailer_check_count != trailer_count:
                raise ValueError("SR count for truck {} does not match. Please Fix it in the file.".format(truck_number))

        except ValueError as err:
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
            errors.append(str(err))
        return errors

    def load_date(self, header):
        date = header[DATE_START:DATE_END]
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        return date_object
