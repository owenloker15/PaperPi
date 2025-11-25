import json
from flask import current_app, render_template
from plugins.baseplugin import BasePlugin
from utils.render_utils import screenshot_html
import requests
import icalendar
import recurring_ical_events
from datetime import datetime, timedelta, date
import calendar


class CalendarPlugin(BasePlugin):
    def __init__(self, id, name):
        super().__init__(id, name)

    def render_image(self, plugin_settings, app):
        calendar_urls = plugin_settings["calendarURLs[]"]
        calendar_colors = plugin_settings["calendarColors[]"]
        calendar_layout = plugin_settings["layout"]

        start, end = self._get_start_end(calendar_layout)
        events = self._create_events(calendar_urls, calendar_colors, start, end)
        print(events)

        with app.app_context():
            str = render_template(
                "calendar/display/display.html", settings=plugin_settings, events=events
            )
            image = screenshot_html(str)
            display_manager = current_app.config["Display_Manager"]
            display_manager.update_display(image)

    def _create_events(self, calendar_urls, calendar_colors, start, end):
        cleaned_events = []
        for calendar_url, calendar_color in zip(calendar_urls, calendar_colors):
            calendar = self._fetch_calendar(calendar_url)
            events = recurring_ical_events.of(calendar).between(start, end)
            cleaned_events.extend(self._clean_events(events, calendar_color))
        return cleaned_events

    def _fetch_calendar(self, calendar_url) -> icalendar.Calendar:
        try:
            response = requests.get(calendar_url)
            response.raise_for_status()
            return icalendar.Calendar.from_ical(response.text)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch iCalendar url: {str(e)}")

    def _get_start_end(self, calendar_layout):
        current_dt = datetime.today().date()

        if calendar_layout == "timeGridDay":
            start = datetime.combine(current_dt, datetime.min.time())
            end = start + timedelta(days=1)
        elif calendar_layout == "timeGridWeek":
            # start on Sunday
            start_date = current_dt - timedelta(days=current_dt.weekday() + 1)
            start = datetime.combine(start_date, datetime.min.time())
            end = start + timedelta(days=7)
        elif calendar_layout in ("dayGridMonth", "listMonth"):
            # first day of month
            start_date = current_dt.replace(day=1)
            start = datetime.combine(start_date, datetime.min.time())

            # last day + 1 (exclusive end)
            month_end = calendar.monthrange(current_dt.year, current_dt.month)[1]
            end_date = current_dt.replace(day=month_end) + timedelta(days=1)
            end = datetime.combine(end_date, datetime.min.time())
        else:
            raise ValueError(f"Unsupported layout: {calendar_layout}")

        return start, end


    def _clean_events(self, events, color):
        event_list = []

        for event in events:
            summary = str(event.get("SUMMARY"))
            dtstart = event.get("DTSTART").dt
            dtend = event.get("DTEND").dt if event.get("DTEND") else None
            all_day = False

           # Normalize datetime/date to ISO strings
            if isinstance(dtstart, datetime):
                start_str = dtstart.isoformat()
            elif isinstance(dtstart, date):
                start_str = dtstart.isoformat()
                all_day = True
            else:
                continue  # skip unknown type

            event_dict = {
                "title": summary,
                "start": start_str,
                "allDay": all_day,
            }

            if dtend:
                if isinstance(dtend, datetime):
                    end_str = dtend.isoformat()
                elif isinstance(dtend, date):
                    # FullCalendar treats all-day end as exclusive
                    # so if ical says 2025-09-18, you might want +1 day
                    end_str = dtend.isoformat()
                event_dict["end"] = end_str

            event_dict["color"] = color

            event_list.append(event_dict)

        return event_list

