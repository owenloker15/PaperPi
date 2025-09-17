import json
from flask import render_template
from plugins.baseplugin import BasePlugin
from utils.render_utils import screenshot_html
import requests
import icalendar
import recurring_ical_events
from datetime import datetime, timedelta
import calendar


class CalendarPlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)

    def render_image(self, plugin_settings, app):
        calendar_url = plugin_settings["calendarUrl"]
        calendar_layout = plugin_settings["layout"]

        start, end = self._get_start_end(calendar_layout)
        events = self._create_events(calendar_url, start, end)
        plugin_settings["events"] = json.dumps(events)
        print(plugin_settings['events'])

        with app.app_context():
            str = render_template(
                "calendar/display/display.html", settings=plugin_settings
            )
            screenshot_html(str)

    def _create_events(self, calendar_url, start, end):
        calendar = self._fetch_calendar(calendar_url)
        events = recurring_ical_events.of(calendar).between(start, end)
        cleaned_events = self._clean_events(events)
        return cleaned_events

    def _fetch_calendar(self, calendar_url) -> icalendar.Calendar:
        try:
            response = requests.get(calendar_url)
            response.raise_for_status()
            return icalendar.Calendar.from_ical(response.text)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch iCalendar url: {str(e)}")

    def _get_start_end(self, calendar_layout):
        # timezone = pytz.timezone("America/New_York")
        current_dt = datetime.today().date()
        if calendar_layout == "timeGridDay":
            start = current_dt
            end = current_dt
        elif calendar_layout == "timeGridWeek":
            # + 1 for Sunday start
            start = current_dt - timedelta(days=current_dt.weekday() + 1)
            end = start + timedelta(days=6)
        elif calendar_layout == "timeGridMonth" or calendar_layout == "listMonth":
            start = current_dt.replace(day=1)
            month_end = calendar.monthrange(current_dt.year, current_dt.month)[1]
            end = current_dt.replace(day=month_end)
        else:
            print("unsupported")

        return start, end

    def _clean_events(self, events):
        event_list = []

        for event in events:
            summary = str(event.get("SUMMARY"))
            dtstart = event.get("DTSTART").dt
            dtend = event.get("DTEND").dt if event.get("DTEND") else None

            # Convert datetimes to ISO strings (FullCalendar friendly)
            event_dict = {
                "title": summary,
                "start": dtstart.isoformat(),
            }
            if dtend:
                event_dict["end"] = dtend.isoformat()

            event_list.append(event_dict)
        
        return event_list
