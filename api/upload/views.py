from rest_framework import status
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


class Upload(APIView):
    permission_classes=(IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format="txt"):
        msg = {}
        file_obj = request.FILES["file"]
        lines = list(file_obj.__iter__())
        warning, date = load_header(lines[0], "cool")
        if not warning:
            msg["result"] = "Good"
        else:
            msg["Warning"] = warning
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



def load_cities(city_file):
    
