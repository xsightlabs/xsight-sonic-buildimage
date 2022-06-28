DEVICE_DATA = {
    'x86_64-es9632xx-r0': {
        'thermal': {
            'threshold_table': {
                "thermal_U31_x48":   {"-127:68:1":5, "69:74:2":10, "75:84:3":10, "85:120:4":10},
                "thermal_U61_x49":   {"-127:65:1":5, "66:70:2":10, "71:80:3":10, "81:120:4":10},
                "thermal_U86_x4A":   {"-127:58:1":5, "59:63:2":10, "64:83:3":10, "84:120:4":10},
                "asic_average":      {"-127:89:1":5, "90:104:2":10, "105:114:3":10, "115:120:4":10}
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
    },
    'x86_64-es9632xq-r0': {
        'thermal': {
            'threshold_table': {
                "thermal_U31_x48":   {"-127:68:1":5, "69:90:2":10, "91:95:3":10, "96:120:4":10},
                "thermal_U61_x49":   {"-127:65:1":5, "66:86:2":10, "87:91:3":10, "92:120:4":10},
                "thermal_U86_x4A":   {"-127:58:1":5, "59:76:2":10, "77:81:3":10, "82:120:4":10},
                "asic_average":      {"-127:89:1":5, "90:104:2":10, "105:114:3":10, "115:120:4":10}
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

