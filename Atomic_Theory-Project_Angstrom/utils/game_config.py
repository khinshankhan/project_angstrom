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
- max: maximum number of times that action can be performed (for validation, can be None)
- min: minimum number of times that action can be performed (for validation)
'''

GAME_AUTO_2018 = {
    '00_g_auto' : {
        'name': 'Glyphs in Auto',
        'type': NUM,
        'points': 15,
        'icon': 'add_box',
        'max': None,
        'min': 0
    },
    '01_jewel_auto': {
        'name': 'Jewel',
        'type': NUM,
        'points': 30,
        'icon': 'add_circle',
        'max': 1,
        'min': 0
    },
    '02_park_auto': {
        'name': 'Safe Zone Park',
        'type': BOOL,
        'points': 10,
        'icon': 'local_parking',
        'max': 1,
        'min': 0
    },
    '03_key_auto': {
        'name': 'Cryptobox Key',
        'type': BOOL,
        'points': 30,
        'icon': 'vpn_key',
        'max': 1,
        'min': 0
    }
}

GAME_TELE_2018 = {
    '04_g_tele': {
        'name': 'Glyphs in Teleop',
        'type': NUM,
        'points': 2,
        'icon': 'add_box',
        'max': 24,
        'min': 0
    },
    '05_row_tele': {
        'name': 'Rows of Glyphs',
        'type': NUM,
        'points': 10,
        'icon': 'keyboard_arrow_right',
        'max': 8,
        'min': 0
    },
    '06_col_tele': {
        'name': 'Columns of Glyphs',
        'type': NUM,
        'points': 20,
        'icon': 'keyboard_arrow_up',
        'max': 6,
        'min': 0
    },
    '07_cipher_tele': {
        'name': 'Ciphers Completed',
        'type': NUM,
        'points': 30,
        'icon': 'border_all',
        'max': 2,
        'min': 0
    },
    '08_r1_end': {
        'name': 'Relics in Zone 1',
        'type': NUM,
        'points': 10,
        'icon': 'android',
        'max': 2,
        'min': 0
    },
    '09_r2_end': {
        'name': 'Relics in Zone 2',
        'type': NUM,
        'points': 20,
        'icon': 'android',
        'max': 2,
        'min': 0
    },
    '10_r3_end': {
        'name': 'Relics in Zone 3',
        'type': NUM,
        'points': 40,
        'icon': 'android',
        'max': 2,
        'min': 0
    },
    '11_rup_end': {
        'name': 'Relics Upright',
        'type': NUM,
        'points': 15,
        'icon': 'android',
        'max': 2,
        'min': 0
    },
    '12_bal_end': {
        'name': 'Robot Balanced',
        'type': BOOL,
        'points': 20,
        'icon': 'code',
        'max': 1,
        'min': 0
    }
}
