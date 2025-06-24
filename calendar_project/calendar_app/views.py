# from django.shortcuts import render
# from calendar import HTMLCalendar
# from datetime import datetime, date
# from .utils import get_stored_status

# class StatusCalendar(HTMLCalendar):
#     def formatday(self, day, weekday):
#         if day == 0:
#             return '<td class="noday">&nbsp;</td>'

#         this_date = date(self.year, self.month, day)
#         status = get_stored_status(this_date)

#         if status == "success":
#             color = "green"
#         elif status == "failure":
#             color = "red"
#         else:
#             return f'<td style="padding:10px;">{day}</td>'  # no color

#         return f'<td style="background-color:{color}; padding:10px;">{day}</td>'

#     def formatmonth(self, year, month, withyear=True):
#         self.year, self.month = year, month
#         return super().formatmonth(year, month, withyear)

# def calendar_view(request):
#     now = datetime.now()
#     year = now.year
#     month = now.month

#     cal = StatusCalendar()
#     html_calendar = cal.formatmonth(year, month)

#     return render(request, 'calendar_app/calendar.html', {
#         'calendar': html_calendar,
#         'month': month,
#         'year': year
#     })




# =============================================================



# from django.shortcuts import render
# from calendar import HTMLCalendar
# from datetime import datetime, date
# from .utils import load_status_data

# class StatusCalendar(HTMLCalendar):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data

#     def formatday(self, day, weekday):
#         if day == 0:
#             return '<td class="noday">&nbsp;</td>'

#         this_date = date(self.year, self.month, day).isoformat()
#         status_data = self.data.get(this_date, {})
#         color = "green" if status_data else "white"

#         return f'<td style="background-color:{color}; padding:10px;" class="calendar-cell" data-date="{this_date}">{day}</td>'

#     def formatmonth(self, year, month, withyear=True):
#         self.year, self.month = year, month
#         return super().formatmonth(year, month, withyear)

# def calendar_view(request):
#     now = datetime.now()
#     year = now.year
#     month = now.month
#     data = load_status_data()

#     cal = StatusCalendar(data)
#     html_calendar = cal.formatmonth(year, month)

#     return render(request, 'calendar_app/calendar.html', {
#         'calendar': html_calendar,
#         'status_data': data,
#         'month': month,
#         'year': year
#     })




# =================================================================================



# from django.shortcuts import render
# from calendar import HTMLCalendar
# from datetime import datetime, date
# from .utils import load_status_data

# class StatusCalendar(HTMLCalendar):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data

#     def formatday(self, day, weekday):
#         if day == 0:
#             return '<td class="noday">&nbsp;</td>'

#         this_date = date(self.year, self.month, day).isoformat()
#         status_info = self.data.get(this_date, {})
#         status = status_info.get("status", "").lower()

#         # Determine background color
#         if status == "success":
#             color = "lightgreen"
#         elif status == "failure":
#             color = "lightcoral"
#         else:
#             color = "white"

#         return f'<td style="background-color:{color}; padding:10px;" class="calendar-cell" data-date="{this_date}">{day}</td>'

#     def formatmonth(self, year, month, withyear=True):
#         self.year, self.month = year, month
#         return super().formatmonth(year, month, withyear)

# def calendar_view(request):
#     now = datetime.now()
#     year = now.year
#     month = now.month
#     data = load_status_data()

#     cal = StatusCalendar(data)
#     html_calendar = cal.formatmonth(year, month)

#     return render(request, 'calendar_app/calendar.html', {
#         'calendar': html_calendar,
#         'status_data': data,
#         'month': month,
#         'year': year
#     })





# ============================================



import json
from datetime import datetime, date
from django.shortcuts import render
from .utils import StatusCalendar


def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    with open('status_history.json', 'r') as f:
        status_data = json.load(f)

    # Filter events by selected month
    filtered_data = {
        k: v for k, v in status_data.items()
        if datetime.strptime(k, "%Y-%m-%d").year == year and datetime.strptime(k, "%Y-%m-%d").month == month
    }

    cal = StatusCalendar(filtered_data).formatmonth(year, month)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        'calendar': cal,
        'status_data': json.dumps(status_data),
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'calendar_app/calendar.html', context)
