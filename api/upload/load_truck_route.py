from django.db import IntegrityError
from constants.trailer import *
from constants.truck_route import *
from constants.header import *
from truck_route.models import TruckRoute
from routes.models import Route
from trucks.models import Truck
from datetime import datetime

class LoadTruckRoute:

    def load_truck_route(self, truck_route_file):
        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []
        #Traverse the trucks line by line
        date = self.load_date(truck_route_file[0])
        count = 0
        for data in truck_route_file[1:-1]:
            count += 1
            try:
                truck_route = {}
                truck_route["truck_number"] = int(data[TRUCK_NUM_S:TRUCK_NUM_E])
                truck_route["route_number"] = int(data[ROUTE_NUM_S:ROUTE_NUM_E])
                truck_route["date_added"] = date
                #Check if the truck number exists
                if not Truck.objects.filter(truck_number=truck_route["truck_number"]):
                    raise ValueError("Truck number {} does not exist")
                #Check if the route number exists
                if not Route.objects.filter(route_number=truck_route["route_number"]):
                    raise ValueError("Route number {} does not exist")
                try:
                    #Save the truck route to the database
                    db_truck_route = TruckRoute.objects.create(**truck_route)
                except IntegrityError as err:
                    error = "Rout {} is already assigned to truck {}".format(truck_route["route_number"], truck_route["truck_number"])
                    errors["data"].append(error)
            except ValueError as err:
                error = str(err)
                errors["data"].append(error)

        #Check if the trailer count matches
        errors["trailer"] += self.load_trailer(truck_route_file[-1], count)
        return errors

    def load_date(self, header):
        date = header[DATE_START:DATE_END]
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        return date_object

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

