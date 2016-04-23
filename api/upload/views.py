#Django imports
from rest_framework import status
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#Load scripts imports
from load_cities import LoadCities
from load_routes import LoadRoutes
from load_daily_inventory import LoadDailyInventory
from load_trucks import LoadTrucks
from load_truck_route import LoadTruckRoute
from load_events import LoadEvents
from load_truck_inventory import LoadTruckInventory
from load_default import LoadDefault

#Other imports
from datetime import datetime
import re

class Upload(APIView):
    permission_classes=(IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format="txt"):
        msg = {}
        msg["warnings"] = []
        msg["errors"] = []

        file_obj = request.FILES["file"]
        file_name = file_obj.name
        lines = list(file_obj.__iter__())
        warning = False
#        warning, date = load_header(lines[0], file_name)

        if not warning:
            errors = {}
            if file_name == "cityUpload.txt":
                obj = LoadCities()
                errors = obj.load_cities(lines[1:])
            elif file_name == "routeUpload.txt":
                obj = LoadRoutes()
                errors = obj.load_routes(lines[1:])
            elif file_name == "dailyInventory.txt":
                obj = LoadDailyInventory()
                errors = obj.load_inventory(lines[1:])
            elif file_name == "truckUpload.txt":
                obj = LoadTrucks()
                errors = obj.load_trucks(lines[1:])
            elif file_name == "truckRouteUpload.txt":
                obj = LoadTruckRoute()
                errors = obj.load_truck_route(lines)
            elif file_name == "events.txt":
                obj = LoadEvents()
                errors = obj.load_events(lines)
            elif file_name == "loadTruck.txt":
                obj = LoadTruckInventory()
                errors = obj.load_truck_inventory(lines)
            elif file_name == "loadDefault.txt":
                obj = LoadDefault()
                errors = obj.load_default(lines)
            #Add the errors to all cumulitive errors
            msg["errors"] = errors
        else:
            msg["warnings"] = warning
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(msg, status=status.HTTP_200_OK)


def load_header(header, file_type):
    from constants.header import *
    #If we import events then don't do anything
    if file_type == "events.txt":
        return False, None
    warning = False
    try:
        #Check if header name is HD
        sequence_number = header[SEQUENCE_START:SEQUENCE_END]
        #Check if the sequence number is greater then the last sequence number
        date = header[DATE_START:DATE_END]
        #Check if the date is equal or greater then the last uploaded data
        #Check if the date fits the format
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError as err:
        warning = str(err)
        date_object = ""

    return warning, date_object

def load_trailer(trailer, trailer_check_count):
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









    
