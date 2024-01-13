from dataclasses import dataclass
from components.event_manager.event_body import EventBody


@dataclass
class EventManager:

    def publish(self, body: EventBody):
        raise NotImplementedError

    def consume(self, callback):
        raise NotImplementedError
