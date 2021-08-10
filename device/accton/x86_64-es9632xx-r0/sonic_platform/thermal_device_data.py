DEVICE_DATA = {
    'es9632xx-O32x400G': {
        'thermal': {
            'minimum_table': {
                "unk_trust":   {"-127:30":13, "31:40":14 , "41:120":15},
                "unk_untrust": {"-127:25":13, "26:30":14 , "31:47":16, "48:120":19}
            }
        },
        'fans': {
            'drawer_num': 4,
            'drawer_type': 'real',
            'fan_num_per_drawer': 2,
            'support_fan_direction': False,
            'hot_swappable': True
        },
        'psus': {
            'psu_num': 2,
            'fan_num_per_psu': 1,
            'hot_swappable': True,
            'led_num': 1
        }
    }
}

