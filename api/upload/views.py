from rest_framework import status
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from cities.models import City
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
                errors = load_cities(lines[1:])
            #Add the errors to all cumulitive errors
            msg["errors"] = errors
        else:
            msg["warnings"] = warning
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(msg, status=status.HTTP_200_OK)


def load_header(header, file_type):
    from constants.header import *
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

def load_cities(city_file):
    #Emply the City table
    City.objects.all().delete()
    errors = {}
    errors["data"] = []
    errors["trailer"] = []
    #Traverse the cities line by line
    count = 0
    for line in city_file[:-1]:
        #Increment count to check against
        count += 1

        city = {}
        finds = list(re.search('(.{20})(.{20})(.{2})',line).groups())
        city["city_label"] = finds[0].strip()
        city["city_name"] = finds[1].strip()
        city["state"] = finds[2].strip()

        if not City.objects.filter(city_label=city["city_label"]):
            db_city = City(**city)
            db_city.save()
        else:
            error = "City label, {}, is a duplicate".format(city["city_label"])
            errors["data"].append(error)

    errors["trailer"] += load_trailer(city_file[-1], count)

    return errors







    
