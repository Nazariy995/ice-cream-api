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
from load_sales import LoadSales
SKIP_FILES = ["events.txt", "loadDefault.txt"]
#Other imports
from upload.models import Upload as UploadModel
from datetime import datetime
import re
from pytz import timezone
eastern = timezone('US/Eastern')
import logging
log = logging.getLogger(__name__)

class Upload(APIView):
    permission_classes=(IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format="txt"):
        msg = {}
        msg["warnings"] = []
        msg["errors"] = []
        try:
            file_obj = request.FILES["file"]
            file_name = file_obj.name
            lines = list(file_obj.__iter__())
    #            warning = False
            #Check if teh header is correct
            warning, date = load_header(lines[0], file_name)

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
                elif file_name == "dailySales.txt":
                    obj = LoadSales()
                    errors = obj.load_sales(lines)
                else:
                    errors["data"] = []
                    errors["trailer"] = []
                    msg["errors"]= errors
                    msg["warnings"].append("Please provide the correct file")
                    return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    #            Add the errors to all cumulitive errors
                msg["errors"] = errors
            else:
                log.error(warning)
                msg["warnings"] = [warning]
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            log.error(str(e))
            msg["warnings"].append("Something is wrong with the file. Pleaes check the format of the file")
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        return Response(msg, status=status.HTTP_200_OK)


def load_header(header, file_type):
    from constants.header import *
    #If we import events then don't do anything
    if file_type in SKIP_FILES:
        return False, None

    warning = False
    try:
        sequence_number = int(header[SEQUENCE_START:SEQUENCE_END])

        date = header[DATE_START:DATE_END]

        date_object = datetime.strptime(date, '%Y-%m-%d').date()

        last_upload = UploadModel.objects.filter(file_type=file_type).first()
        #If it is not the initial file then we need to do some checking
        if last_upload:
            last_upload_sequence = last_upload.sequence_number
            if last_upload.sequence_number == 9999:
                last_upload_sequence = 0
            if date_object < last_upload.date_added:
                raise ValueError("Date is less then the previous upload date {}".format(str(last_upload.date_added)))
            if sequence_number - last_upload_sequence != 1:
                raise ValueError("Sequence number must be next up from the last upload of sequence {}".format(last_upload.sequence_number))
            last_upload.sequence_number = sequence_number
            last_upload.date_added = date_object
            last_upload.save()
#        If all the checks are passed save it in the database
        else:
            new_upload = {}
            new_upload["sequence_number"] = sequence_number
            new_upload["file_type"] = file_type
            new_upload["date_added"] = date_object
            db_upload = UploadModel.objects.create(**new_upload)
    except ValueError as err:
        warning = str(err)
        date_object = None

    return warning, date_object










    
