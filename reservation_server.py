import json
import socket 
import ReservationParser as res_parser ## Import parser
import activity_server
import room_server
import os

## HTTP Error messages initialized
general_404_err = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<html><head><title>Error</title></head><body><h1>Page Not Found</h1></body></html>"
general_400_err = "HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n<html><head><title>Bad Request</title></head><body></body></html>"


def room_reserver(parser_response):

    JSON_FNAME="activities.json"
    JSON_FPATH= os.getcwd() + '/'
    JSON_ATTR_ACTIVITIES="activities"
    JSON_ATTR_ACT_NAME="activity_name"

    activity_name = parser_response[3]
    server_response = activity_server.is_activity_exists(activity_name,JSON_FNAME,JSON_FPATH,JSON_ATTR_ACTIVITIES,JSON_ATTR_ACT_NAME)
    if "200 OK" in server_response:

      JSON_FNAME="rooms.json"
      JSON_FPATH=os.getcwd() + '/'
      JSON_ATTR_ROOMS="rooms"
      JSON_ATTR_ROOM_NAME="room_name"
      JSON_ATTR_SCHED="schedule"
      JSON_ATTR_DAY="day"
      JSON_ATTR_UNRES="unres_hours" 
      JSON_ATTR_RES="res_hours" 

      """If exists, then it contacts with the Room Server and tries to reserve the
      room for the specified date/hour/duration. If any of the input is invalid, it sends back an HTTP
      400 Bad Request message. If all the inputs are valid, then it either reserves the room and sends
      back an HTTP 200 OK message, or it sends back an HTTP 403 Forbidden message indicating
      that the room is not available. If the room is reserved, a reservation_id is generated (which can be
      an integer), and an entry is stored for the reservation_id."""
      room_name = parser_response[2]
      day = parser_response[4]
      hour = parser_response[5]  
      duration = parser_response[6] 
      server_response = room_server.reserve_room(room_name,day,hour,duration,
                      JSON_FNAME,JSON_FPATH,JSON_ATTR_ROOMS,JSON_ATTR_ROOM_NAME,
                      JSON_ATTR_SCHED,JSON_ATTR_DAY,JSON_ATTR_UNRES,JSON_ATTR_RES)

      if "200 OK" in server_response:

        JSON_FNAME="reservations.json"
        JSON_FPATH=os.getcwd() + '/'
        JSON_ATTR_RESERVATIONS="reservations"
        JSON_ATTR_RESERVATION_ID="reservation_id"
        JSON_ATTR_ROOM_NAME="room_name"
        JSON_ATTR_ACT_NAME="activity_name"
        JSON_ATTR_DAY="day"
        JSON_ATTR_INTERVAL="interval" 

        interval= f"{hour}:00 - {int(hour)+int(duration)}:00"
        try:
          with open(f"{JSON_FPATH}{JSON_FNAME}", "r") as f:
            json_reservation_database = json.load(f)
            res_length = len(json_reservation_database[JSON_ATTR_RESERVATIONS])
            RESERVATION_TO_BE_ADDED={
              "reservation_id": res_length,
              "room_name": room_name,
              "activity_name": activity_name,
              "day": day,
              "hour": hour,
              "interval": interval
            }   
            json_reservation_database[JSON_ATTR_RESERVATIONS].append(RESERVATION_TO_BE_ADDED)

          with open(f"{JSON_FPATH}{JSON_FNAME}", "w") as f:
            json.dump(json_reservation_database,f)
            return f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>Reservation Added</h1><p>Reservation added with {RESERVATION_TO_BE_ADDED}.</p></body></html>"
        except:
          return general_404_err
      else:
        return server_response

    else:
      return  server_response


"""/listavailability?room=roomname: Lists all the available hours for all days of the week (after
contacting the Room Server probably several times). (HTTP 200 OK is returned in success. In
case of error relevant error messages will be sent as described above)."""

def list_availablity_day(parser_response):
    room_name = parser_response[2]
    day = parser_response[3]
    JSON_FNAME="rooms.json"
    JSON_FPATH=os.getcwd() + '/'
    JSON_ATTR_ROOMS="rooms"
    JSON_ATTR_ROOM_NAME="room_name"      
    JSON_ATTR_SCHED="schedule"
    JSON_ATTR_DAY="day"
    JSON_ATTR_UNRES="unres_hours" 
    JSON_ATTR_RES="res_hours" 

    server_response = room_server.check_availability(room_name,day,
                      JSON_FNAME,JSON_FPATH,JSON_ATTR_ROOMS,JSON_ATTR_ROOM_NAME,
                      JSON_ATTR_SCHED,JSON_ATTR_DAY,JSON_ATTR_UNRES)

    return server_response

"""Lists all the available hours for all days of the week (after
contacting the Room Server probably several times). (HTTP 200 OK is returned in success. In
case of error relevant error messages will be sent as described above)."""
def list_availablity(parser_response):
    room_name = parser_response[2]
    JSON_FNAME="rooms.json"
    JSON_FPATH=os.getcwd() + '/'
    JSON_ATTR_ROOMS="rooms"
    JSON_ATTR_ROOM_NAME="room_name"      
    JSON_ATTR_SCHED="schedule"
    JSON_ATTR_DAY="day"
    JSON_ATTR_UNRES="unres_hours" 
    JSON_ATTR_RES="res_hours" 
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    result = []
    for i in range(1,7):

      server_response = room_server.check_availability(room_name,i,
                        JSON_FNAME,JSON_FPATH,JSON_ATTR_ROOMS,JSON_ATTR_ROOM_NAME,
                        JSON_ATTR_SCHED,JSON_ATTR_DAY,JSON_ATTR_UNRES)
      body = server_response.split("-")[2]
      iterate_day = f"{days_of_week[i-1]}: {body}"
      result.append(iterate_day)
    
    printed_result = ('\n'.join(map(str, result)))

    return f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\nAvailable hours for the {room_name} on\n\n{printed_result}"

def display_reservation_id(parser_response):

    JSON_FNAME="reservations.json"
    JSON_FPATH=os.getcwd() + '/'
    JSON_ATTR_RESERVATIONS="reservations"
    JSON_ATTR_RESERVATION_ID="reservation_id"
    JSON_ATTR_ROOM_NAME="room_name"
    JSON_ATTR_ACT_NAME="activity_name"
    JSON_ATTR_DAY="day"
    JSON_ATTR_HOUR="hour" 
    JSON_ATTR_DURATION = "duration"
    res_id = parser_response[2]
    res_details = {}
    LIST_200_OK = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><p>Details about Reservation with id {res_id} is {res_details}.</p></body></html>"
    LIST_403_FORBIDDEN = f"HTTP/1.1 403 Forbidden\nContent-Type: text/html\n\n<html><body><h1>Error</h1><p>A reservation with the id {res_id} does not exists in the database.</p></body></html>"

    with open(f"{JSON_FPATH}{JSON_FNAME}", "r") as f:
      json_database = json.load(f)

    reservations = json_database[JSON_ATTR_RESERVATIONS]
    found_flag = False
    for i, reservation in enumerate(reservations):
      if str(reservation[JSON_ATTR_RESERVATION_ID]) == str(res_id):
        found_flag = True
        res_details = reservation
        break

    if not found_flag:
      return LIST_403_FORBIDDEN

    return f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><p>Details about Reservation with id {res_id} is {res_details}.</p></body></html>"



"""
This method represents the process of server listening for the client
There are some variables defined which are useful to connect our JSON Database.
"""
def reservation_server_listen(BUFF_SIZE,ADDR,FORMAT,RESERVATION_SERVER):

    """
        While server listening the incomning requests from clients, 
        if a proper request comes,the server should interact with the our simple database(JSON File). 
        Therefore, there are some necessary initializations exists below for accessing the JSON Database
    """
    JSON_FNAME="reservations.json"
    JSON_FPATH=os.getcwd() + '/'
    JSON_ATTR_RESERVATIONS="reservations"
    JSON_ATTR_RESERVATION_ID="reservation_id"
    JSON_ATTR_ROOM_NAME="room_name"
    JSON_ATTR_ACT_NAME="activity_name"
    JSON_ATTR_DAY="day"
    JSON_ATTR_INTERVAL="interval" 

    while True:
        socket , address = RESERVATION_SERVER.accept()                                                             ## accept client
        print("\n-------------> [CONNECTION ACCCEPTED HOST IP || ADDRESS] --> " , socket ," || ",address)   ## server log message
        message=socket.recv(BUFF_SIZE).decode(FORMAT)                                                       ## get client's message
        if not str(message.split('\n')[0].split(' ')[1]).startswith("/favicon.ico"):                        ## preventing web browser icon 
          print(f"\n-------------> [CLIENT MESSAGE CAME BELOW] -->\n\n{message}")                           ## server log message
        
        ############################################################ Berin Part ############################################################

        server_response = ""
        parser_response=res_parser.main(message)

        try:
          if str(parser_response[0])==str(400):
                server_response=general_400_err
        
          elif str(parser_response[0])==str(404):
                server_response = general_404_err

          elif str(parser_response[0])==str(200):     

            if str(parser_response[1])=="reserve":
                server_response=room_reserver(parser_response)
            elif str(parser_response[1])=="listavailability":
              if (len(parser_response) == 3):
                  server_response=list_availablity(parser_response)
              else:
                  server_response=list_availablity_day(parser_response)
            elif str(parser_response[1])=="display":
                server_response=display_reservation_id(parser_response)
        except Exception as e:
          server_response=general_404_err  


        

        socket.send(server_response.encode(FORMAT))                                                                   ## sending proper http response to client
        print("-------------> [SENDING MESSAGE TO CLIENT] --> PROPER HTTP MESSAGE WILL BE SHOWN IN THE WEB BROWSER")  ## server log message
        socket.close()                                                                                                ## end session
        print(f"\n-------------> [CONNECTION CLOSING] --> Connection with {address} ended!")                          ## server log message
        print("\n*****************************************************************************************************************************")


## Main method
if __name__ == "__main__":

    ## Socket attributes initializations
    BUFF_SIZE = 2048                                                  ## set the chunk size
    PORT = 5050                                                       ## set port for server
    SERVER = socket.gethostbyname(socket.gethostname())               ## get hos ip
    ADDR = (SERVER, PORT)                                             ## fully address tupple
    FORMAT = 'utf-8'                                                  ## encode/decode format
    
    ## Room Server necessary initializations    
    RESERVATION_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ## create socket
    RESERVATION_SERVER.bind(ADDR)                                            ## binding
    RESERVATION_SERVER.listen()                                              ## server up
    print(f"\n////////////////////////// -> SERVER IS CREATED AND READY TO LISTEN WITH THE ADDRESS OF {ADDR}] <- \\\\\\\\\\\\\\\\\\\\\\\\\\\n")
    reservation_server_listen(BUFF_SIZE,ADDR,FORMAT,RESERVATION_SERVER)