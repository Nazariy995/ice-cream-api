
from default_inventory.models import DefaultInventory
from warehouse_inventory.models import WarehouseInventory
MAX_ITEMS=5

class LoadDefault:

    def load_default(self, default_file):
        errors = {}
        errors["data"] = []
        errors["trailer"] = []
        #Delete all the past default items
        DefaultInventory.objects.all().delete()

        for line in default_file:
            line = line.split(",")
            db_default = {}
            try:
                db_default["item_number"] = int(line[0].strip())
                db_default["quantity"] = int(line[1].strip())
                print db_default
                if not WarehouseInventory.objects.filter(item_number=db_default["item_number"]):
                    raise Exception("Item {} does not exist in current warehouse inventory".format(db_default["item_number"]))
                count = DefaultInventory.objects.all().count()
                if count > 5:
                    raise Exception("Maximum value of {} was exceeded for the default_inventory".format(MAX_ITEMS))
                new_inv = DefaultInventory.objects.create(**db_default)
            except Exception as e:
                error = str(e)
                errors["data"].append(error)

        return errors
