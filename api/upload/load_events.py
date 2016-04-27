
from events.models import Event
from datetime import datetime

class LoadEvents:
    '''
    Warren, Polish Summer Festival,2016-07-20
    City, Name, Date(YYYY-MM-DD)
    '''

    def load_events(self, events_file):
        #Delete all the past evnets
        self.delete_events()

        #Initiate errors
        errors = {}
        errors["data"] = []
        errors["trailer"] = []

        for event in events_file:
            #Split the data based on the comma
            event = event.split(",")
            temp_event = {}
            temp_event["city"] =  event[0].strip()
            temp_event["name"] = event[1].strip()
            date = event[2].strip()
            date_object = datetime.strptime(date, '%Y-%m-%d').date()
            temp_event["date"] = date_object
            #Create the event in the database
            db_event = Event.objects.create(**temp_event)

        return errors

    def delete_events(self):
        Event.objects.all().delete()


