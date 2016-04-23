
from default_inventory.models import DefaultInventory

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
                new_inv = DefaultInventory.objects.create(**db_default)
            except Exception as e:
                error = str(e)
                errors["data"].append(error)

        return errors
