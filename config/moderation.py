from copy import deepcopy
from models.protection import Protection
from models.enums import UserLevel, PenaltyType

@staticmethod
def get_protections():
    return deepcopy(_PROTECTIONS)

_PROTECTIONS = {
    'links': Protection(
        name='links',
        description='Elimina los mensajes que puedan contener enlaces hacia otros sitios.',
        penalty=PenaltyType.DELETE_MESSAGE,
        reason='Por seguridad, no esta permitido enviar links.',
        exclude=UserLevel.MODERATOR,
        duration=0,
        strikes=0
    ),

    'repeated_messages': Protection(
        name='repeated messages',
        description='Detecta si un usuario ha enviado el mismo mensaje insistentemente.',
        penalty=PenaltyType.TIME_OUT,
        reason='Spam: Envío repetitivo de mensajes idénticos.',
        exclude=UserLevel.MODERATOR,
        duration=0,
        strikes=3
    ),

    'long_messages': Protection(
        name='long messages',
        description='Elimina los mensajes que son demasiado extensos.',
        penalty=PenaltyType.DELETE_MESSAGE,
        reason='Envió de mensaje demasiado largo.',
        exclude=UserLevel.MODERATOR,
        max_length=300,
        duration=0,
        strikes=0
    )
}