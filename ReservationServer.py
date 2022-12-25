import re

DAY_LIST = ['1', '2', '3', '4', '5', '6', '7']
HOUR_LIST = ['9', '10', '11', '12', '13', '14', '15', '16', '17']
NOT_FOUND = ['404']
BAD_REQUEST = ['400']

MAIN_PATTERN = ':\d{4}\/(.*)\?'
RESERVE_PATTERN = '\d+\/reserve\?room=([^&]*)&activity=([^&]*)&day=([^&]*)&hour=([^&]*)&duration=([^&]*)&{0,1}$'
AVAILABILITY_PATTERN = '\d+\/listavailability\?room=([^&]*)&day=([^&]*)&{0,1}$'
AVAILABILITY_PATTERN2 = '\d+\/listavailability\?room=([^&]*)&day=([^&]*)&{0,1}$'
DISPLAY_PATTERN = '\d+\/diplay\?id=([^&]*)&{0,1}$'
