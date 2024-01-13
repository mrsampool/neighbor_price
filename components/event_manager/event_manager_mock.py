from dataclasses import dataclass
from typing import List

from components.event_manager.event_body import EventBody
from components.event_manager.event_manager import EventManager


@dataclass
class EventManagerMock(EventManager):

    def __init__(self, publish_list: List[EventBody]):
        super().__init__()
        self.published: List[EventBody] = publish_list

    def publish(self, body: EventBody):
        self.published.append(body)