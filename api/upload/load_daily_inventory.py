from constants.daily_inventory import *
from warehouse_inventory.models import WarehouseInventory
from constants.trailer import *
import logging
log = logging.getLogger(__name__)

class LoadDailyInventory:

    def load_inventory(self, inventory_file):
        errors = {}
        errors["data"] = []
        errors["trailer"] = []
#        self.delete_inventory()
        count = 0

        for line in inventory_file[:-1]:
            count += 1
            item = {}
            item["item_number"] = int(line[ITEM_NUM_S:ITEM_NUM_E])
            try:
                item["quantity"] = int(line[WAREHOUSE_Q_S:WAREHOUSE_Q_E])
                item["price"] = int(line[PRICE_S:PRICE_E])/100.0
                item["description"] = line[DESCR_S:DESCR_E].strip()
                db_item = WarehouseInventory.objects.filter(item_number=item["item_number"]).first()
                if db_item:
                    if item["description"]:
                        db_item.description = item["description"]
                    if item["price"] > 0:
                        db_item.price = item["price"]
#                        db_item.quantity = item["quantity"]
                        db_item.save()
                else:
                    if item["quantity"] < 0:
                        raise ValueError("Quantity is less then zero")
                    if not item["description"]:
                        raise ValueError("Description not available")
                    if item["price"] < 0:
                        raise ValueError("Price is less then 0")

                    db_item = WarehouseInventory.objects.create(**item)
            except ValueError as err:
                error = str(err) + " when adding item {}".format(item["item_number"])
                log.error(error)
                errors["data"].append(error)

        errors["trailer"] += self.load_trailer(inventory_file[-1], count)

        return errors

    def delete_inventory(self):
        WarehouseInventory.objects.all().delete()

    def load_trailer(self, trailer, trailer_check_count):
        errors = []
        try:
            #Convert trailer count to a number
            trailer_count = int(trailer[TR_NUM_S:TR_NUM_E])
            #Check if the trailer count match
            if trailer_check_count != trailer_count:
                raise ValueError("Trailer count does not match. Please Fix it in the file.")

        except ValueError as err:
            errors.append(str(err))
            log.error(str(err))

        return errors
