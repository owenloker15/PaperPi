from datetime import datetime, timedelta

from flask import current_app


def parse_form(request_form):
    request_dict = request_form.to_dict()
    for key in request_form.keys():
        if key.endswith("[]"):
            request_dict[key] = request_form.getlist(key)
    return request_dict


def json_to_timedelta(data):
    seconds = data.get("seconds", 0)
    minutes = data.get("minutes", 0)
    hours = data.get("hours", 0)
    days = data.get("days", 0)

    return timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)


def next_active_plugin(playlist, app):
    app_config = app.config["Configuration"]
    plugin_configs = app_config.get_plugin_configs()

    schedules = []
    for plugin_config in plugin_configs:
        plugin_id = plugin_config.get("id")
        schedule_settings = playlist.get_plugin_schedule(plugin_id)
        schedule_settings["id"] = plugin_id
        schedules.append(schedule_settings)

    current_datetime = datetime.now()
    closest_plugin = None
    closest_time = None

    for schedule in schedules:
        daily_time_str = schedule.get("dailyTime")

        if not daily_time_str:
            continue

        daily_time = datetime.strptime(daily_time_str, "%H:%M").time()

        scheduled_datetime = datetime.combine(current_datetime.date(), daily_time)

        if scheduled_datetime <= current_datetime:
            scheduled_datetime += timedelta(days=1)

        time_diff = scheduled_datetime - current_datetime

        if closest_time is None or time_diff < closest_time:
            closest_time = time_diff
            closest_plugin = schedule["id"]

    return closest_plugin
