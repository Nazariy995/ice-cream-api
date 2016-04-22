from constants.trailer import *
import re
from cities.models import City
from routes.models import Route

class LoadCities:
    
    def load_cities(self, city_file):
        #Emply the City table
        self.delete_cities()

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

        errors["trailer"] += self.load_trailer(city_file[-1], count)

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
    
    def delete_cities(self):
        City.objects.all().delete()
        Route.objects.all().delete()
