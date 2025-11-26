from datetime import timedelta


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
