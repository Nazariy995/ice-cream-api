from constants.routes import *
from constants.trailer import *
from cities.models import City
from routes.models import Route

class LoadRoutes:

    def load_routes(self, route_file):
        ACTIONS = {
            "A":self.add_route
        }
        errors = {}
        errors["data"] = []
        errors["trailer"] = []
        count = 0
        #Traverse the routes line by line
        for line in route_file[:-1]:
            count += 1
            temp_errors = []
            action = line[ACTION_S:ACTION_E]
            route_number = int(line[ROUTE_N_S:ROUTE_N_E])
            cities = []
            city_start_location = CITIES_S
            while city_start_location < len(line):
                city_end_location = city_start_location + CITIES_L
                city = line[city_start_location:city_end_location].strip()
                cities.append(city)
                city_start_location = city_end_location

            if action in ACTIONS:
                func = ACTIONS.get(action, None)
                temp_errors += func(cities, route_number)
            else:
                error = "Action for route number {} is not allowed"
                temp_errors.append(error)

            errors["data"] += temp_errors

        errors["trailer"] += self.load_trailer(route_file[-1], count)

        return errors

    #Add cities to Route
    def add_route(self, cities, route_number):
        errors = []
        from constants.routes import *
        print "Add route"
        if len(cities) <= MAX_CITIES and len(cities) > 0:
            route = Route.objects.filter(route_number=route_number)
            if not route:
                route = Route.objects.create(route_number=route_number)
                for city in cities:
                    db_city = City.objects.filter(city_label=city, route__isnull=True).first()
                    if db_city:
                        db_city.route = route
                        db_city.save()
                    else:
                        error = "City {} in route number {} does not exist or is already assigned".format(city, route_number)
                        #delte the cities that were just assigned
                        City.objects.filter(route=route).delete()
                        errors.append(error)
                        break
            else:
                error = "Route number {} already exists in the database".format(route_number)
                errors.append(error)
        else:
            error = "Route number {} either contains more than {} or not enough cities".format(route_number, MAX_CITIES)
            errors.append(error)

        return errors

    def load_trailer(self, trailer, trailer_check_count):
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




