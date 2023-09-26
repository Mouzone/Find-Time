from datetime import datetime


class Timespan:

    def __init__(self, event, start_time, end_time):
        self.event = event
        self.startTime = self.convert_to_datetime(start_time)
        self.endTime = self.convert_to_datetime(end_time)

    def set_event(self, event):
        # Event: boolean (false means free time)
        self.event = event

    def set_start_time(self, start_time):
        self.startTime = start_time

    def set_end_time(self, end_time):
        self.endTime = end_time

    def get_event(self):
        return self.event

    def get_start_time(self):
        return self.startTime

    def get_end_time(self):
        return self.endTime

    def get_time_duration(self):
        duration = self.endTime - self.startTime
        return duration.total_seconds() / 3600  # Convert to hours

    @staticmethod
    def convert_to_datetime(time_var):
        if isinstance(time_var, str):
            time_var = datetime.strptime(time_var, "%Y-%m-%dT%H:%M:%S%z")
        return time_var

    def classify_event_time(self):
        hours_in_morning = 0
        hours_in_afternoon = 0
        hours_in_evening = 0
        if self.get_time_duration() > 24:
            return "Multi-Day Event"
        hours_list = list(range(self.startTime.hour, self.endTime.hour+1))
        for i in hours_list:
            if i < 12:
                hours_in_morning += 1
            elif i < 17:
                hours_in_afternoon += 1
            elif i >= 17:
                hours_in_evening += 1
        if hours_in_morning >= hours_in_afternoon and hours_in_morning >= hours_in_evening:
            return "Morning"
        elif hours_in_afternoon >= hours_in_morning and hours_in_afternoon >= hours_in_evening:
            return "Afternoon"
        elif hours_in_evening >= hours_in_morning and hours_in_evening >= hours_in_afternoon:
            return "Evening"

    def print_timespan(self):
        print(self.event)
        print("Start Time: ", self.startTime)
        print("End Time: ", self.endTime)
        print("Time Duration: ", self.get_time_duration())
        print("Time of Day: ", self.classify_event_time())
