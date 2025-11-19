from copy import deepcopy
from models.eventsub import EventSub

def get_event_subs() -> dict[str, EventSub]:
    return deepcopy(_EVENT_SUBS)

_EVENT_SUBS = {
    'stream.offline': EventSub(
        name='Stream offline',
        description='Se dispara cuando el canal del streamer termina la transimición.'
    ),
    'stream.online': EventSub(
        name='Stream online',
        description='Se dispará cuando el canal del streamer comienza una transmición en vivo.'
    ),
    'channel.follow': EventSub(
        name='Channel follow',
        description='EL canal del emisor recibe un nuevo seguidor.'
    ),
    'channel.subscribe': EventSub(
        name='Channel subscription',
        description='El canal del emisor recibe una nueva suscripción.'
    )
}