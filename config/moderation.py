from copy import deepcopy
from models.protection import Protection
from models.enums import UserLevel, PenaltyType

@staticmethod
def get_protections():
    return deepcopy(_PROTECTIONS)

_PROTECTIONS = {
    'links': Protection(
        name='links',
        penalty=PenaltyType.DELETE_MESSAGE,
        reason='Por seguridad, no esta permitido enviar links.',
        exclude=UserLevel.MODERATOR,
        duration=0,
        strikes=0,
    ),

    'repeated_messages': Protection(
        name='repeated_messages',
        penalty=PenaltyType.TIME_OUT,
        reason='Spam: Envío repetitivo de mensajes idénticos.',
        exclude=UserLevel.MODERATOR,
        duration=0,
        strikes=3
    ),

    'long_messages': Protection(
        name='long_messages',
        penalty=PenaltyType.DELETE_MESSAGE,
        reason='Envió de mensaje demasiado largo.',
        exclude=UserLevel.MODERATOR,
        max_length=300,
        duration=0,
        strikes=0
    )
}