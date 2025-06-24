
# import json
# from datetime import date
# import os

# STATUS_FILE = os.path.join(os.path.dirname(__file__), "status_history.json")

# def load_status_data():
#     try:
#         with open(STATUS_FILE, "r") as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}

# def get_stored_status(check_date: date) -> str:
#     data = load_status_data()
#     return data.get(check_date.isoformat(), "")




# ==================================


# import json
# import os

# STATUS_FILE = os.path.join(os.path.dirname(__file__), "status_history.json")

# def load_status_data():
#     try:
#         with open(STATUS_FILE, "r") as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {}


# ========================================


from calendar import HTMLCalendar
from datetime import date


class StatusCalendar(HTMLCalendar):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        this_date = date(self.year, self.month, day).isoformat()
        status_info = self.data.get(this_date, {})
        status = status_info.get("Slapi status", "").lower()

        if status == "success":
            color = "lightgreen"
        elif status == "failure":
            color = "lightcoral"
        else:
            color = "white"

        return f'<td style="background-color:{color}; padding:10px;" class="calendar-cell" data-date="{this_date}">{day}</td>'

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super().formatmonth(year, month, withyear)
