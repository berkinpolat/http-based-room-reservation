import re

def checkValues(variables):
    day = variables[1]
    hour = variables[2]
    duration = variables[3]
    if day in ['1', '2', '3', '4', '5', '6', '7']:
        if hour in ['9', '10', '11', '12', '13', '14', '15', '16', '17']:
            try:
                hour = int(hour)
                day = int(day)
                duration = int(duration)
            except ValueError:
                print('int değil')
            if (duration > 0) and (9 <= (hour + duration)) and (17 >= (hour + duration)):
                return True
    return False

pattern = '\d+\/reserve\?name=([^\s;\/?:@&=$,]*)&day=([^\s;\/\.?:@&=$,]*)&hour=([^\s;\/\.?:@&=$,]*)&duration=([^\s;\/\.?:@&=$,]*)&*'
request = "http://192.168.1.79:5050/reserve?name=M2Z05&day=2&hour=9&duration=2"

try:
    variables = re.search(pattern, request).groups()
    if not checkValues(variables):
        raise AttributeError
except AttributeError:
    print("Bad Request")
    exit()

print("mrb")
