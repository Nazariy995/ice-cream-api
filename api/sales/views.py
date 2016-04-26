from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sales.models import Sales
from truck_route.models import TruckRoute
from datetime import datetime, date
from pytz import timezone
from django.db.models import Sum, Count
eastern = timezone('US/Eastern')
import sendgrid

class SalesView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self, request):
        data = request.data
        msg = {}
        msg["errors"] = []
        sales = []
        try:
            print data
            start_date = get_date(data["start_date"])
            print start_date
            end_date = get_date(data["end_date"])
            get_all = data["get_all"]
            get_trucks = data["get_trucks"]
            get_routes = data["get_routes"]
            if start_date > end_date:
                raise Exception("Please provide a start date that is less then the end date")
            sales = sales_by_day(start_date, end_date, get_all, get_trucks, get_routes)

        except Exception as e:
            msg["errors"].append("Please specify the correct start and end date")
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(sales, status=status.HTTP_200_OK)


def sales_by_day(start_date, end_date, get_all=False, get_trucks=False, get_routes=False):
    print start_date
    print end_date
    sales = Sales.objects.filter(date_added__range=[start_date,end_date]).order_by("-date_added")
    print sales
    print "YEs"
    if get_trucks:
        sales = sales.values('truck_route__truck_number', 'date_added').annotate(revenue=Sum('revenue'), sold=Sum('quantity_sold'))
    elif get_routes:
        sales = sales.values('truck_route__route_number', 'date_added').annotate(revenue=Sum('revenue'), sold=Sum('quantity_sold'))
    elif get_all:
        print "Woohoooo"
        sales = sales.values('date_added').annotate(revenue=Sum('revenue'), sold=Sum('quantity_sold'))
    else:
        return []

    sales = format_sales(sales)
    return sales

def format_sales(sales):
    formatted_sales = []
    for sale in sales:
        temp_sale = {}
        temp_sale["start_date"] = sale["date_added"]
        temp_sale["end_date"] = sale["date_added"] if "end_date" not in sale else sale["end_date"]
        if "truck_route__truck_number" in sale:
            temp_sale["truck_number"] = sale["truck_route__truck_number"]
        if "truck_route__route_number" in sale:
            temp_sale["route_number"] = sale["truck_route__route_number"]
        temp_sale["revenue"] = sale["revenue"]
        temp_sale["sold"] = sale["sold"]
        formatted_sales.append(temp_sale)
    return formatted_sales

def get_date(date_string):
    try:
        print date_string
        date_object = datetime.strptime(date_string, '%d/%m/%Y').date()
        return date_object
    except:
        raise Exception("Please provide the correct date")




