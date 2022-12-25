import re

# . al ama float olmasin
# sonda parametre ekleme
# parametre 0'dan büyük olcak -> uzunluk
# değerler yanlış: 400
# link yanlış: 404

DAY_LIST = ['1', '2', '3', '4', '5', '6', '7']
HOUR_LIST = ['9', '10', '11', '12', '13', '14', '15', '16', '17']
NOT_FOUND = ['404']
BAD_REQUEST = ['400']

MAIN_PATTERN = '\d+\/(.*)\?'
RESERVE_PATTERN = '\d+\/reserve\?name=([^\s;\/?:@&=$,]*)&day=([^\s;\/?:@&=$,]*)&hour=([^\s;\/?:@&=$,]*)&duration=([^\s;\/?:@&=$,]*)&{0,1}'
ADD_PATTERN = '\d+\/add\?name=([^\s;\/?:@&=$,]*)&{0,1}'
REMOVE_PATTERN = '\d+\/remove\?name=([^\s;\/?:@&=$,]*)&{0,1}'
AVAILABILITY_PATTERN = '\d+\/checkavailability\?name=([^\s;\/?:@&=$,]*)&day=([^\s;\/?:@&=$,]*)&{0,1}'


# GENERAL PURPOSE FUNCTIONS
def ListContainsNull(variable_list):
    for item in variable_list:
        if item:
            continue
        else:
            return True
    return False


def ListContainsAlphanumericCharacter(variable_list):
    for item in variable_list:
        if re.search(r'[^0-9a-zA-Z]', item):
            return True
    return False


def checkHourAndDurationRule(hour, duration):
    try:
        hour = int(hour)
        duration = int(duration)
    except ValueError:
        return False
    if (duration > 0) and (9 <= (hour + duration)) and (17 >= (hour + duration)):
        return True
    else:
        return False

"""
# RESERVE ROOM HELPER FUNCTIONS
def checkReserveValues(variable_list):
    name = variable_list[0]
    day = variable_list[1]
    hour = variable_list[2]
    duration = variable_list[3]

    if day in DAY_LIST:
        if hour in HOUR_LIST:
            try:
                hour = int(hour)
                day = int(day)
                duration = int(duration)
            except ValueError:
                return False
            if (duration > 0) and (9 <= (hour + duration)) and (17 >= (hour + duration)):
                return True
    return False
"""
"""
# RESERVE ROOM MAIN FUNCTION
def reserve(request):
    try:
        variables = re.search(RESERVE_PATTERN, request).groups()

    except AttributeError:
        return NOT_FOUND

    response = checkReserveValues(variables)

    if not response:
        return BAD_REQUEST
    else:
        return response

"""
# ADD-REMOVE-AVAILABILITY HELPER FUNCTIONS
def checkValues(variable_list):
    # check if any variable is null
    if ListContainsNull(variable_list):
        return False

    # check if variables contain any non-alphanumeric character
    if ListContainsAlphanumericCharacter(variable_list):
        return False

    if len(variable_list) >= 2:
        if not variable_list[1] in DAY_LIST:
            return False
    if len(variable_list) == 4:
        if not variable_list[2] in HOUR_LIST:
            return False
        if not checkHourAndDurationRule(variable_list[2], variable_list[3]):
            return False

    return True


# FUNCTION
def check404(request, get_type):
    pattern = ""
    if get_type == "add":
        pattern = ADD_PATTERN
    elif get_type == "remove":
        pattern = REMOVE_PATTERN
    elif get_type == "reserve":
        pattern = RESERVE_PATTERN
    elif get_type == "checkavailability":
        pattern = AVAILABILITY_PATTERN
    else:
        return NOT_FOUND

    try:
        variables = re.search(pattern, request).groups()

    except AttributeError:
        return NOT_FOUND

    response = checkValues(variables)

    if not response:
        return BAD_REQUEST
    else:
        response = ['200']
        for variable in variables:
            response.append(variable)
        return response


def main(request):
    try:
        get_type = re.search(MAIN_PATTERN, request).group(1)

        if get_type in ["add", "remove", "reserve", "checkavailability"]:
            return check404(request, get_type)
        else:
            raise AttributeError

    except AttributeError:
        return NOT_FOUND


# ADD TEST
print(main("http://192.168.1.79:5050/add?name=M2Z05"))

# REMOVE TEST
print(main("http://192.168.1.79:5050/remove?name=M2Z05"))

# RESERVE TEST
print(main("http://192.168.1.79:5050/reserve?name=M2Z05&day=3&hour=9&duration=1"))

# AVAILABILITY TEST
print(main("http://192.168.1.79:5050/checkavailability?name=M2Z05&day=3"))
