from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    __title: str

    def get_title(self):
        return self.__title



s = Song("Matargasti")
print(s.get_title())


class Iterator(ABC):

    @abstractmethod
    def has_next(self): pass

    @abstractmethod
    def next(self): pass


class PlaylistItr(Iterator):

    def __init__(self, song_list: List[Song]):

        self.__songlist = song_list
        self.__position = 0


    def has_next(self):
        return self.__position < len(self.__songlist)

    def next(self) -> Song | None:
        while self.has_next():
            s = self.__songlist[self.__position] 
            self.__position += 1
            return s

        return None

@dataclass
class Playlist:

    __name: str
    __playlist: List[Song]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name


    def add_song(self, song: Song):
        self.__playlist.append(song)

    def get_iterator(self) -> PlaylistItr:
        return PlaylistItr(self.__playlist)


pl = Playlist("Imitiaz Ali", [Song("Agar Tum Saath Ho"), Song("Hawaa Hawaa")])

pl_itr = pl.get_iterator()
while pl_itr.has_next():
    print(f"Playing {pl_itr.next().get_title()}")
