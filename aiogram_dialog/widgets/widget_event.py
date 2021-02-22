from typing import Union, Callable, Any

from aiogram_dialog.manager.intent import ChatEvent
from aiogram_dialog.manager.protocols import DialogManager
from aiogram_dialog.widgets.action import Actionable


class WidgetEventProcessor:
    def process_event(self, event: ChatEvent, source: Any, manager: DialogManager, *args, **kwargs):
        pass


class SimpleEventProcessor(WidgetEventProcessor):
    def __init__(self, callback: Callable):
        self.callback = callback

    def process_event(self, event: ChatEvent, source: Any, manager: DialogManager, *args, **kwargs):
        if self.callback:
            self.callback(event, source, manager, *args, **kwargs)


def ensure_event_processor(processor: Union[Callable, WidgetEventProcessor, None]) -> WidgetEventProcessor:
    if isinstance(processor, WidgetEventProcessor):
        return processor
    else:
        return SimpleEventProcessor(processor)