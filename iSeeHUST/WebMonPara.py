# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic
# CreateDate : 2017-06-20


APP_CONFIG = {
    'HARD_TIME_LIMITER': 10080,
    'HARD_AMOUNT_LIMITER': 15,
    'DB_SCHEMA': 'schema.sql',
    'FETCH_INTERVAL': 60,          # Default data fetch interval(minutes)
    'DEFAULT_DATE_RANGE': 30,      # Maximum date range displayed in Flask page
    'NIGHT_SHIFT': True,    # The app will run at a increased interval at night
    'WEEKEND_SHIFT': True,    # The app will run at a increased interval during weekend
    'OFFSHIFT_INTERVAL': 360,       # Data fetch interval during night and weekend(minutes)
    'SHIFT_START': 7,
    'SHIFT_END': 18,
    'MAX_LOG_SIZE': 512             # Max log size in KB
}

DB_CONFIGS = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'iSeeHUST',
    'charset': 'utf8'
}