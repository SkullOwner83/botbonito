from copy import deepcopy
from models.protection import Protection
from models.enums import UserLevel

@staticmethod
def get_protections():
    return deepcopy(_PROTECTION)

_PROTECTION = {
    'links': Protection(
        name='links',
        penalty='delete_message',
        reason='Por seguridad, no esta permitido enviar links.',
        exclude=UserLevel.MODERATOR,
        duration=0,
        strikes=0,
    ),

    'repeated_messages': Protection(
        name='repeated_messages',
        penalty='timeout',
        reason='Spam: Envío repetitivo de mensajes idénticos.',
        exclude='no_one',
        duration=0,
        strikes=3
    ),

    'long_messages': Protection(
        name='long_messages',
        penalty='delete_message',
        reason='Envió de mensaje demasiado largo.',
        exclude='no_one',
        max_length=300,
        duration=0,
        strikes=0
    )
}