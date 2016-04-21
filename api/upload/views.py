from rest_framework import status
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class Upload(APIView):
    permission_classes=(IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format="txt"):

        file_obj = request.FILES["file"]
        lines = list(file_obj.__iter__())
        for line in lines[1:-1]:
            print line
        msg = {
            "result":"Technical dificulties!"
        }

        return Response(msg, status=status.HTTP_200_OK)
