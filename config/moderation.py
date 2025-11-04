from copy import deepcopy
from models.protection import Protection
from utilities.enums import UserLevel, PenaltyType

@staticmethod
def get_protections() -> dict [str, Protection]:
    return deepcopy(_PROTECTIONS)

_PROTECTIONS = {
    'links': Protection(
        name='links',
        description='Elimina los mensajes que puedan contener enlaces hacia otros sitios.',
        penalty=PenaltyType.DELETE_MESSAGE.value,
        reason='Por seguridad, no esta permitido enviar links.',
        exclude=UserLevel.MODERATOR.value,
        duration=0,
        strikes=0
    ),

    'repeated_messages': Protection(
        name='repeated_messages',
        description='Detecta si un usuario ha enviado el mismo mensaje insistentemente.',
        penalty=PenaltyType.TIME_OUT.value,
        reason='Spam: Envío repetitivo de mensajes idénticos.',
        exclude=UserLevel.MODERATOR.value,
        duration=0,
        strikes=3
    ),

    'long_messages': Protection(
        name='long_messages',
        description='Elimina los mensajes que son demasiado extensos.',
        penalty=PenaltyType.DELETE_MESSAGE.value,
        reason='Envío de mensaje demasiado largo.',
        exclude=UserLevel.MODERATOR.value,
        threshold=300,
        duration=0,
        strikes=0
    ),

    'excess_caps': Protection(
        name='excess_caps',
        description='Elimina los mensajes escritos con exceso de mayusculas.',
        penalty=PenaltyType.DELETE_MESSAGE.value,
        reason='Envio de mensaje con uso excesivo de mayusculas.',
        exclude=UserLevel.MODERATOR.value,
        threshold=0.8,
        duration=0,
        strikes=0
    ),

    'excess_symbols': Protection(
        name='excess_symbols',
        description='Limita el número de simbolos o caracteres especiales permitidos por mensaje.',
        penalty=PenaltyType.DELETE_MESSAGE.value,
        reason='Envio de mensaje con uso excesivo de simbolos.',
        exclude=UserLevel.MODERATOR.value,
        threshold=0.8,
        duration=0,
        strikes=0
    ),

    'excess_emotes': Protection(
        name='excess_emotes',
        description='Limita el número de emotes por mensaje para evitar spam.',
        penalty=PenaltyType.DELETE_MESSAGE.value,
        reason='Envio de mensaje con uso excesivo de emotes.',
        exclude=UserLevel.MODERATOR.value,
        threshold=30,
        duration=0,
        strikes=0
    ),
}