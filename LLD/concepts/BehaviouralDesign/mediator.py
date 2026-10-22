from abc import ABC, abstractmethod
from typing import List



class Flight:

    def __init__(self, flight_number: str, controlTower: 'ControlTower'):
        self.__flight_number = flight_number
        self.__controlTower = controlTower
        self.__controlTower.register_flight(self)


    @property
    def flightno(self):
        return self.__flight_number

    @property
    def ctfullname(self):
        return f"{self.__controlTower.ctname}_{self.__controlTower.location}"


    def message_for_controlTower(self, message: str):
        self.__controlTower.acknowledge_message(self, message)

    def message_for_other_flights(self, message: str):
        self.__controlTower.broadcast_message(self, message)

    def broadcast_from_another_flight(self, sender: 'Flight', message: str):
        print(f"Broadcast Message: {message} from Flight: {sender.flightno} to {self.flightno}")

    def broadcast_from_controlTower(self, message: str):
        print(f"Broadcast Message: {message} from ControlTower: {self.ctfullname} to {self.flightno}")

    def ooo_from_controlTower(self, message):
        print(f"OOO Message: {message} from controltower: {self.ctfullname} to {self.flightno}")

    def relay_message_from_flight(self, message, sender: 'Flight'):
        print(f"Relay Message: {message} from Flight: {sender.flightno} to {self.flightno}")

    def relay_message_to_flight(self, message, recieverflightno: str):
        self.__controlTower.relay_message(self, message, recieverflightno)




class ATC(ABC):

    @abstractmethod
    def register_flight(self, flight: Flight): pass

    @abstractmethod
    def broadcast_message(self, sender: Flight, message: str): pass

    @abstractmethod
    def ooo_message(self, message: str, reciever_flight_number: str): pass

    @abstractmethod
    def relay_message(self, sender: Flight, message: str, reciever_flight_number: str): pass

    @abstractmethod
    def acknowledge_message(self, sender: Flight, message: str): pass



class ControlTower(ATC):

    def __init__(self, name, location):
        self.__name: str = name
        self.__location: str = location
        self.__flightList: List[Flight] = []


    @property
    def ctname(self):
        return self.__name

    @property
    def location(self):
        return self.__location


    def register_flight(self, flight):
        self.__flightList.append(flight)


    def broadcast_message(self, sender: Flight, message):
        for fl in self.__flightList:
            if fl.flightno != sender.flightno:
                fl.broadcast_from_another_flight(sender, message)


    def ooo_message(self, message, reciever_flight_number):
        for fl in self.__flightList:
            if fl.flightno == reciever_flight_number:
                fl.ooo_from_controlTower(message)



    def relay_message(self, sender, message, reciever_flight_number):
        for fl in self.__flightList:
            if fl.flightno == reciever_flight_number:
                fl.relay_message_from_flight(message, sender)


    def acknowledge_message(self, sender, message):
        print(f"Message: {message} recieved from flight {sender.flightno}")
        



controltower = ControlTower("Terminal 2", "Jaipur, RJ")

indigo = Flight("6E2521", controltower)
spicejet = Flight("SP2020", controltower)
airexpress = Flight("AIRINDIA101", controltower)


indigo.message_for_other_flights("Hey Guys, Whats up!")
indigo.relay_message_to_flight("Sales ho nahi rahi tumhari", "SP2021")