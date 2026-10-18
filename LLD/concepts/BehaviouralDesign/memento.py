from dataclasses import dataclass
from typing import List

@dataclass
class TextMemento:
    _text: str

    def get_text(self) -> str:
        return self._text

@dataclass
class History:
    _history: List[TextMemento]

    def __init__(self):
        self._history = []

    def save_state(self, tm: TextMemento):
        self._history.append(tm)

    def see_history(self):
        for tm in self._history:
            print(f"{tm.get_text()}")


    def undo(self):
        if len(self._history) == 0:return TextMemento("")

        self._history.pop()

        if len(self._history) == 0:return TextMemento("")
        return self._history[-1]



class TextEditor:
    _text: str

    def __init__(self):
        self._text = ""

    def write(self, text):
        self._text += text

    def get_text(self) -> str:
        return self._text

    def save(self) -> TextMemento:
        return TextMemento(self._text)

    def restore(self, tm: TextMemento):
        self._text = tm.get_text()

    


te = TextEditor()
history = History()

te.write("Hello")
te.write(" Mememto")

history.save_state(te.save())
te.write(" Pattern")

history.save_state(te.save())

history.see_history()

te.restore(history.undo())
print(te.get_text())
