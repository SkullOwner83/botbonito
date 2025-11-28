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
        description='Se dispará cuando el canal del streamer comienza una transmición en vivo.',
        params=['started_at']
    ),
    'channel.follow': EventSub(
        name='Channel follow',
        description='EL canal del emisor recibe un nuevo seguidor.',
        params=['user', 'user_id', 'followed_at']
    ),
    'channel.subscribe': EventSub(
        name='Channel subscription',
        description='El canal del emisor recibe una nueva suscripción.',
        params=['user', 'user_id', 'followed_at']
    ),
    'channel.update': EventSub(
        name='Channel update',
        description='La información del canal del emisor ha sido actualizada.',
        params=['title', 'category', 'language']
    )
}