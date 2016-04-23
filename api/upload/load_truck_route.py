from constants.trailer import *
from constants.truck_route import *
from constants.header import *
from truck_route.models import TruckRoute

class LoadTruckRoute:

    def load_trucks(self, truck_route_file):
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
                truck_route["truck"] = int(data[TRUCK_NUM_S:TRUCK_NUM_E])
                truck_route["route"] = int(data[ROUTE_NUM_S:ROUTE_NUM_E])
                truck_route["date_added"] = date
                db_truck_route = TruckRoute.objects.create(**truck_route)
            except ValueError as err:
                error = str(err)
                errors["data"].append(error)

        #Check if the trailer count matches
        errors["trailer"] += self.load_trailer(truck_route_file[-1], count)

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

