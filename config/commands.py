from copy import deepcopy
from models.commands import CommandConfig
from utilities.enums import UserLevel

@staticmethod
def get_default_commands():
    return deepcopy(_DEFAULT_COMMANDS)

_DEFAULT_COMMANDS = {
    'help': CommandConfig(
        name='help',
        description='Muestra la lista de comandos disponibles que el usuario puede usar.',
        alias=['ayuda'],
        user_level=UserLevel.EVERYONE.value
    ),

    'schedule': CommandConfig(
        name='schedule',
        alias=['horario'],
        description='Muestra el horario de transmisción del emisor.',
        user_level=UserLevel.EVERYONE.value
    ),

    'followage': CommandConfig(
        name='followage',
        description='Muestra la fecha en la que el usuario comenzó a seguir al emisor.',
        alias=[],
        user_level=UserLevel.EVERYONE.value,
        response_type='say'

    ),

    'playsound': CommandConfig(
        name='play',
        alias=[],
        description='Permite al usuario reproducir un sonido en el canal del emisor.',
        user_level=UserLevel.EVERYONE.value
    ),

    'speak': CommandConfig(
        name='speak',
        description='Permite que el bot lea el comentario del usuario en el canal del emisor.',
        alias=['say'],
        max_length=200,
        user_level=UserLevel.EVERYONE.value
    ), 

    'giveaway': CommandConfig(
        name='giveaway',
        description='Permite al emisor iniciar y finalizar la recopilación de usuarios para un sorteo.',
        alias=['sorteo'],
        user_level=UserLevel.BROADCASTER.value
    ),

    'giveaway_entry': CommandConfig(
        name='entry',
        description='Permite a los usuarios entrar en la lista para participar en un sorteo.',
        alias=['leentro'],
        user_level=UserLevel.FOLLOWER.value
    ),

    'feedback': CommandConfig(
        name='feedback',
        description='Permite al emisor iniciar y finalizar una sesión de retroalimentación de creaciones de los usuarios.',
        alias=[],
        user_level=UserLevel.BROADCASTER.value
    ),

    'send': CommandConfig(
        name='send',
        description='Permite a los usuarios enviar un enlace de sus creaciones al emisor para obtener retroalimentación.',
        alias=['demo'],
        user_level=UserLevel.FOLLOWER.value
    ),
}