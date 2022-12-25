import re

DAY_LIST = ['1', '2', '3', '4', '5', '6', '7']
HOUR_LIST = ['9', '10', '11', '12', '13', '14', '15', '16', '17']
NOT_FOUND = ['404']
BAD_REQUEST = ['400']

MAIN_PATTERN = ':\d{4}\/(.*)\?'
RESERVE_PATTERN = '\d+\/reserve\?name=([^&]*)&day=([^&]*)&hour=([^&]*)&duration=([^&]*)&{0,1}'
ADD_PATTERN = '\d+\/add\?name=([^&]*)&{0,1}'
REMOVE_PATTERN = '\d+\/remove\?name=([^&]*)&{0,1}'
AVAILABILITY_PATTERN = '\d+\/checkavailability\?name=([^&]*)&day=([^&]*)&{0,1}'


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


# 400 BAD REQUEST FUNCTION
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


# 404 NOT FOUND FUNCTION
def check404(request, get_type):
    # Select a regex pattern according to the get type
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

    # Parse the request according to the pattern.
    # If it's not parsed without an error, throw a NOT FOUND error.
    try:
        variables = re.search(pattern, request).groups()

    except AttributeError:
        return NOT_FOUND

    # ;\/?:@&=$, are delimiters in URLs, so they shouldn't be used in variable values.
    for item in variables:
        if re.search(r'[\s;\/?:@&=$,]', item):
            return NOT_FOUND

    # Check the correctness of the values.
    # If there is a problem with the values, throw a BAD REQUEST error.
    response = checkValues(variables)

    # If there is a BAD REQUEST, return ['400']
    # If there is no error, return ['200', 'V', ..., 'V'] where 'V' is a value of the request.
    if not response:
        return BAD_REQUEST
    else:
        response = ['200', get_type]
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
print("ADD", main("http://192.168.1.79:5050/add?name=M2Z05"))

# REMOVE TEST
print("REMOVE", main("http://192.168.1.79:5050/remove?name=M2Z05"))

# RESERVE TEST
print("RESERVE", main("http://192.168.1.79:5050/reserve?name=M2Z05&day=7&hour=9&duration=1"))

# AVAILABILITY TEST
print("AVAILABILITY", main("http://192.168.1.79:5050/checkavailability?name=M2Z05&day=3"))
