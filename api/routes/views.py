from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class Routes(APIView):

    def get(self):
        msg = {
            "result":"Technical dificulties!"
        }
        return Response(msg, status=status.HTTP_200_OK)
