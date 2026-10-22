
from abc import ABC, abstractmethod
from dataclasses import dataclass


class TemparatureObserver(ABC):

    @abstractmethod
    def update_temp(self, temp: float):
        raise NotImplementedError()


@dataclass
class PhoneDisplay(TemparatureObserver):

    _temp: float = 0.0

    def update_temp(self, temp: float):
        self._temp = temp
        print(f"Updated temparature for {__class__.__name__}")
        

class WeatherStation:

    _observers: list[TemparatureObserver] = []
    _temp: float = 0.0

    def add_new_device(self, obs: TemparatureObserver):
        self._observers.append(obs)

    def update_temparature(self, new_temp: float):
        self._temp = new_temp
        self.notify_temp_observers(new_temp)

    def notify_temp_observers(self, new_temp):
        for o in self._observers:
            o.update_temp(new_temp)



ws = WeatherStation()
ws.add_new_device(PhoneDisplay())

ws.update_temparature(42.2)


    
