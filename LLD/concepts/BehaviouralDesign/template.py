from abc import ABC, abstractmethod


class DataParser(ABC):
    def _parse(self):
        pass


    def _open(self):
        print("Opening the file")

    def _close(self):
        print("Closing the file")

    @abstractmethod
    def _dataParser(self):
        pass


class CSVParser(DataParser):
    def _dataParser(self):
        print("Parsing CSV Parser")



csv = CSVParser()
csv._parse()

        