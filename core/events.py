import weakref
import collections
import logging
import threading


class Event(object):
    pass


class InitEvent(Event):
    pass


class TickEvent(Event):
    def __init__(self, elapsed_time):
        self.elapsed_time = elapsed_time


class ExitEvent(Event):
    pass


class CloseCurrentModelEvent(Event):
    def __init__(self, next_model_name):
        self.next_model_name = next_model_name


class AttachCharEvent(Event):
    def __init__(self, entity, entity_name, char):
        self.entity = entity
        self.entity_name = entity_name
        self.char = char


class RemoveCharEvent(Event):
    def __init__(self, entity, entity_name, n):
        self.entity = entity
        self.entity_name = entity_name
        self.n = n


class LoginRequestedEvent(Event):
    pass


class EventManager(object):
    """
    Receives event and post them to the listeners.
    """

    def __init__(self):
        self._listeners = weakref.WeakKeyDictionary()
        self._queue = collections.deque()
        self._next_id = 0
        self._sem = threading.Semaphore()
        self.next_model_name = None

    def register_listener(self, listener):
        """
        Register a listener.
        :param listener: the listener
        :return: the listener id
        """
        listener_id = self._next_id
        self._next_id += 1
        self._listeners[listener] = listener_id
        logging.debug("Registered listener %s with id %d." % (listener.__class__.__name__, listener_id))
        return listener_id

    def unregister_listener(self, listener):
        """
        Unregister a listener.
        :param listener: the listener
        """
        if listener in self._listeners:
            del self._listeners[listener]
            logging.debug("Unregistered listener %s." % listener.__class__.__name__)

    def post(self, event):
        """
        Add an event to the event queue.
        :param event: the event
        """
        self._queue.append(event)
        if isinstance(event, TickEvent) or isinstance(event, InitEvent):
            while len(self._queue) > 0:
                ev = self._queue.popleft()

                # Iterate over a copy of the dict, so even from within the loop, listeners can delete themselves.
                for l in list(self._listeners):
                    l.notify(ev)
        elif isinstance(event, CloseCurrentModelEvent):
            self.next_model_name = event.next_model_name