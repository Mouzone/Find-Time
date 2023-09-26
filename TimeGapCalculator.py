from timespan import Timespan
from datetime import datetime, timezone, timedelta

def overlap_calculator(timespans):
    for i in range(len(timespans)-1):
        #if overlap, then make one event that has the early start time and the latest end time
        #then remove the two events that overlapped and make one event in the place in the list
            if timespans[i].get_end_time() > timespans[i+1].get_start_time():
                if timespans[i+1].get_end_time() > timespans[i].get_end_time():
                    overlap_temp = Timespan(True, timespans[i].get_start_time, timespans[i+1].get_end_time)
                else:
                    overlap_temp = Timespan(True, timespans[i].get_start_time, timespans[i].get_end_time)
                timespans.insert(i, overlap_temp)
                timespans.remove(timespans[i+1])
                timespans.remove(timespans[i+2])

    return timespans


def freetime_calculator(timespans, deadline):
    current_time = datetime.now(timezone.utc)
    deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%S.%f%z")
    free_time_list = []

    free_time_list.append(Timespan(False, current_time, timespans[0].get_start_time()))
    for i in range(len(timespans) - 1):
        free_time_list.append(Timespan(False, timespans[i].get_end_time(), timespans[i+1].get_start_time()))

    if deadline > timespans[-1].get_start_time():
        free_time_list.append(Timespan(False, timespans[-1].get_end_time(), deadline))

    return free_time_list


