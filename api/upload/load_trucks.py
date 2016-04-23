import re
from constants.trailer import *
from trucks.models import Truck

class LoadTrucks:
    
    def load_trucks(self, truck_file):
        #Delete all the Trucks
#        self.delete_trucks()

        errors = {}
        errors["data"] = []
        errors["trailer"] = []
        #Traverse the trucks line by line
        count = 0
        for line in truck_file[:-1] :
            count += 1
            finds = list(re.search('(.{4})',line).groups())
            truck = {}
            truck["truck_number"] = int(finds[0].strip())
            #Get or create the truck object in the database
            truck, created = Truck.objects.get_or_create(**truck)

        #Check if the trailer count matches
        errors["trailer"] += self.load_trailer(truck_file[-1], count)

        return errors

    
    def load_trailer(self, trailer, trailer_check_count):
        errors = []
        try:
            #Convert trailer count to a number
            trailer_count = int(trailer[TR_NUM_S:TR_NUM_E])
            #Check if the trailer count matches
            if trailer_check_count != trailer_count:
                raise ValueError("Trailer count does not match. Please Fix it in the file.")

        except ValueError as err:
            errors.append(str(err))

        return errors

    #Purpose: Delete all trucks from the database
    def delete_trucks(self):
        Truck.objects.all().delete()
