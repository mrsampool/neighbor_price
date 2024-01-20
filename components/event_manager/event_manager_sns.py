from dataclasses import dataclass
from components.event_manager.event_manager import EventManager
from components.event_manager.event_body import EventBody


@dataclass
class EventManagerSNS(EventManager):

    def publish(self, body: EventBody):
        raise NotImplementedError

    def consume(self, callback):
        raise NotImplementedError
