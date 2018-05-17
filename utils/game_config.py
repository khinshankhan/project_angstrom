# CONSTANTS
NUM = 0
BOOL = 1
STRING = 2

'''
SPECIFICATIONS FOR GAME TASKS:
- id: unique identifier for the task
- name: name of task (to be displayed)
- type: type of data recorded (see constants above)
- points: number of points the action gives
- icon (OPTIONAL): material icon corresponding to the task (from google)
'''

GAME_AUTO_2018 = [
    {
        'id': 'g_auto',
        'name': 'Glyphs in Auto',
        'type': NUM,
        'points': 15,
        'icon': 'add_box'
    },
    {
        'id': 'jewel_auto',
        'name': 'Jewel',
        'type': NUM,
        'points': 30,
        'icon': 'add_circle'
    },
    {
        'id': 'park_auto',
        'name': 'Safe Zone Park',
        'type': BOOL,
        'points': 10,
        'icon': 'local_parking'
    },
    {
        'id': 'key_auto',
        'name': 'Cryptobox Key',
        'type': BOOL,
        'points': 30,
        'icon': 'vpn_key'
    }
]

GAME_TELE_2018 = [
    {
        'id': 'g_tele',
        'name': 'Glyphs in Teleop',
        'type': NUM,
        'points': 2,
        'icon': 'add_box'
    },
    {
        'id': 'row_tele',
        'name': 'Rows of Glyphs',
        'type': NUM,
        'points': 10,
        'icon': 'keyboard_arrow_right'
    },
    {
        'id': 'col_tele',
        'name': 'Columns of Glyphs',
        'type': NUM,
        'points': 20,
        'icon': 'keyboard_arrow_up'
    },
    {
        'id': 'cipher_tele',
        'name': 'Ciphers Completed',
        'type': NUM,
        'points': 30,
        'icon': 'border_all'
    },
    {
        'id': 'r1_end',
        'name': 'Relics in Zone 1',
        'type': NUM,
        'points': 10,
        'icon': 'android'
    },
    {
        'id': 'r2_end',
        'name': 'Relics in Zone 2',
        'type': NUM,
        'points': 20,
        'icon': 'android'
    },
    {
        'id': 'r3_end',
        'name': 'Relics in Zone 3',
        'type': NUM,
        'points': 40,
        'icon': 'android'
    },
    {
        'id': 'rup_end',
        'name': 'Relics Upright',
        'type': NUM,
        'points': 15,
        'icon': 'android'
    },
    {
        'id': 'bal_end',
        'name': 'Robot Balanced',
        'type': BOOL,
        'points': 20,
        'icon': 'code'
    }
]
