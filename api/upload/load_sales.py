from constants.sales import *
from constants.header import *
from datetime import datetime
from truck_inventory.models import TruckInventory
from truck_route.models import TruckRoute
from sales.models import Sales

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
                errors["data"] += self.add_items(truck_sales)
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

    def add_items(self, truck_sales):
        errors = []
        truck_number = truck_sales["truck_number"]
        date = truck_sales["date"]
        #Check if the Truck has been assigne at the beginnig  of the day
        truck_route = TruckRoute.objects.filter(truck_number=truck_number, date_added=date).first()
        if not truck_route:
            errors.append("Truck number {} was not assigned a route in the morning and should not have sales".format(truck_number))
            return errors
        #continue on
        count = 0
        try:
            total_revenue = 0
            total_sold = 0
            for sale_item in truck_sales["items"]:
                try:
                    item_number = sale_item["item_number"]
                    db_item = TruckInventory.objects.filter(item_number=item_number, truck_number=truck_number, date_added=date).first()
                    #If item did not exists at the start of the day then throw an error
                    if not db_item:
                        raise Exception("Item {} was not at the start of the day inventory".format(item_number))

                    quantity_sold = db_item.quantity - sale_item["quantity"]
                    #If quantity sold is higher then starting quantity or is negative stop
                    if quantity_sold < 0 or quantity_sold > db_item.quantity:
                        raise Exception("Item {} final quantity is either higher then start quantity or is negative".format(item_number))
                    #Add count to increment count of items sold
                    count+=1
                    revenue = db_item.price * quantity_sold
                    total_sold += quantity_sold
                    total_revenue += revenue
                except Exception as e:
                    error = str(e)
                    errors.append(error)
            #Check if the count equals starting inventory count
            start_invetory_count = TruckInventory.objects.filter(truck_number=truck_number, date_added=date).count()
            if start_invetory_count != count:
                raise Exception("Inventory items count for truck {} does not match starting inventory".format(truck_number))
            #Save the sales to the database
            self.save_sales(truck_route, date, total_sold, total_revenue)
        except Exception as e:
            error = str(e)
            errors.append(error)

        return errors

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

    def save_sales(self, truck_route, date, total_sold, total_revenue):
        sales_item = Sales.objects.filter(truck_route=truck_route, date_added=date).first()
        #if the sales for the truck exist
        if sales_item:
            sales_item.quantity_sold = total_sold
            sales_item.total_revenue = total_revenue
            sales_item.save()
        else:
            sales_item = {}
            sales_item["quantity_sold"] = total_sold
            sales_item["revenue"] = total_revenue
            sales_item["truck_route"] = truck_route
            sales_item["date_added"] = date
            Sales.objects.create(**sales_item)
