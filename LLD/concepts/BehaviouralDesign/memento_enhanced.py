"""
Following arjan codes: The Memento pattern: Saving State Without Breaking Encapsulation
"""


from dataclasses import dataclass
from typing import Protocol

class Snapshotable[T](Protocol):

    def snapshot(self) -> T:
        pass

    def restore(self, snapshot: T) -> None:
        pass


class History[T]:

    def __init__(self):
        self._snapshots: list[T] = []

    def save(self, obj: Snapshotable[T]) -> None:
        self._snapshots.append(obj.snapshot())

    def undo(self, obj: Snapshotable[T]) -> bool:
        if not self._snapshots:
            return False

        obj.restore(self._snapshots.pop())

        return True



@dataclass
class Step:
    name: str
    enabled: bool = True


@dataclass
class WorkflowSnapshot:

    name: str
    steps: tuple[Step, ...]


class Workflow:

    def __init__(self, name, steps: list[Step]):
        self._name = name
        self._steps = steps

    def rename(self, name):
        self._name = name

    def add_step(self, step: Step):
        self._steps.append(step)

    def describe(self):
        return f"{self._name}: {[step.name for step in self._steps]}"

    def snapshot(self) -> WorkflowSnapshot:
        return WorkflowSnapshot(self._name, steps=tuple(self._steps))

    def restore(self, snapshot: WorkflowSnapshot):
        self._name = snapshot.name
        self._steps = list(snapshot.steps)



workflow = Workflow("Order Processing", [Step("charge debit card")])

history: History[WorkflowSnapshot] = History()
history.save(workflow)


workflow.rename("Invoice Processing")
workflow.add_step(Step("send_confirmation to email"))


print(f"{workflow.describe()}")
history.undo(workflow)

print(f"{workflow.describe()}")