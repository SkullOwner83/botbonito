from copy import deepcopy
from models.commands import CommandConfig

@staticmethod
def get_default_commands():
    return deepcopy(__DEFAULT_COMMANDS)

__DEFAULT_COMMANDS = {
    'help': CommandConfig(
        name="help",
        alias=["ayuda"],
        user_level="everyone",
    ),

    'schedule': CommandConfig(
        name='schedule',
        alias=['horario'],
        user_level='everyone',
    ),

    'followage': CommandConfig(
        name='followage',
        alias=[],
        user_level='everyone',
        response_type='say'

    ),

    'playsound': CommandConfig(
        name='play',
        alias=[],
        user_level='everyone'
    ),

    'speak': CommandConfig(
        name='speak',
        alias=['say'],
        user_level='everyone'
    ), 

    'giveaway': CommandConfig(
        name='giveaway',
        alias=['sorteo'],
        user_level='broadcaster'
    ),

    'giveaway_entry': CommandConfig(
        name='entry',
        alias=['leentro'],
        user_level='everyone'
    ),

    'feedback': CommandConfig(
        name='feedback',
        alias=[],
        user_level='everyone',
    ),

    'send': CommandConfig(
        name='send',
        alias=['demo'],
        user_level='everyone',
    ),
}