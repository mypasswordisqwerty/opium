#!/usr/bin/env python3
import suntime
import json
import os
from datetime import timedelta, datetime, date

DELTA = 60


def main():
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))
    with open(file) as f:
        conf = json.load(f)
    s = suntime.Sun(conf['latitude'], conf['longitude'])
    en = (s.get_local_sunrise_time() + timedelta(minutes=DELTA)).time()
    st = (s.get_local_sunset_time() - timedelta(minutes=DELTA)).time()
    conf['time_start'] = st.strftime("%H:%M")
    conf['time_end'] = en.strftime("%H:%M")
    with open(file, "w") as f:
        json.dump(conf, f, indent=4)


if __name__ == "__main__":
    main()
