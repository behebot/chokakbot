from datetime import datetime
from pytz import timezone
from collections import defaultdict


class TimeOfDay:
    cost_of_hour = {
        23: 1, 0: 2, 1: 3, 2: 3, 3: 2, 4: 1,
        5: 1, 6: 2, 7: 3, 8: 3, 9: 2, 10: 1,
        11: 1, 12: 2, 13: 3, 14: 3, 15: 2, 16: 1,
        17: 1, 18: 2, 19: 3, 20: 3, 21: 2, 22: 1,
    }

    tod_cost = defaultdict(int)
    debug = False  # set in constructor
    u2tz = {}  # set in constructor
    u2tod = {}

    def __init__(self, u2tz, debug=False):
        self.u2tz = u2tz
        self.debug = debug
        self.fill_all()

    def get_tod(self, hour):
        if hour == 23 or hour <= 4:
            return 'night'
        elif hour >= 5 and hour <= 10:
            return 'morning'
        elif hour >= 11 and hour <= 16:
            return 'day'
        elif hour >= 17 and hour <= 22:
            return 'evening'

    def get_tz_for_user(self, user):
        try:
            result = self.u2tz[user]
        except:
            return "Unknown user {}.".format(user)
        else:
            return result

    def get_user_list(self):
        return self.u2tz.keys()

    def get_hour_for_user(self, user):
        return self.get_hour_for_tz(self.u2tz[user])

    def get_hour_for_tz(self, tz):
        return datetime.now(timezone(tz)).hour

    def get_tod_for_tz(self, tz):
        return self.get_tod(
            self.get_hour_for_tz(tz)
        )

    def fill_all(self):
        for user, tz in self.u2tz.iteritems():
            tod = self.get_tod_for_tz(tz)
            self.u2tod[user] = tod
            self.tod_cost[tod] += self.cost_of_hour[self.get_hour_for_tz(tz)]

    def get_time_of_day(self):
        message = ""
        for user, tod in self.u2tod.iteritems():
            hour = self.get_hour_for_user(user)
            if self.debug:
                message += "User: {}. Hour in his TZ is: {}. " \
                    "ToD there is: {}. Cost is: {}\n" \
                    "".format(user, hour, tod, self.cost_of_hour[hour])
        cur_tod = max(self.tod_cost.iterkeys(),
                      key=(lambda key: self.tod_cost[key]))
        if self.debug:
            message += "By max sum of points ToD is: {}".format(cur_tod)
        else:
            message += "{}".format(cur_tod)
        return message
