from logging import getLogger
import gokart
from my_gokart_example.utils.template import GokartTask

logger = getLogger(__name__)


class Sample(GokartTask):
    def run(self):
        self.dump("sample output")


class StringToSplit(GokartTask):
    """Like the function to divide received data by spaces."""

    task = gokart.TaskInstanceParameter()

    def run(self) -> None:
        sample: str = self.load("task")
        self.dump(sample.split(" "))


class Main(GokartTask):
    """endpoint task."""

    def requires(self):
        return StringToSplit(task=Sample())
