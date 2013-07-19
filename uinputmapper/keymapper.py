# encoding: utf-8
"""
Module to help with creating fast keycode mapping arrays
"""

def parse_keymap(args, rev_event_keys, event_keys):
    """
    Reads in a keymap configuration and returns structures to implement it
    """
    keymap_config = {}
    execfile(args.keymap, keymap_config)
    switch_layout_keys = keymap_config['switch_layout_keys']
    revert_default_key = keymap_config['revert_default_key']
    revert_keymap_index = keymap_config['revert_keymap_index']
    default_keymap_index = keymap_config['default_keymap_index']
    keymaps = keymap_config['keymaps']
    #print keymap_config
    #exit(0)
    #import pprint
    short_to_long = {
        'APP':'COMPOSE',
        'BRK':'BREAK',
        'BSLS':'BACKSLASH',
        'BSPC':'BACKSPACE',
        'CAPS':'CAPSLOCK',
        'COMM':'COMMA',
        'DEL':'DELETE',
        'ENT':'ENTER',
        'EQL':'EQUAL',
        'GRV':'GRAVE',
        'INS':'INSERT',
        'LALT':'LEFTALT',
        'LBRC':'LEFTBRACE',
        'LCTL':'LEFTCTRL',
        'LGUI':'LEFTMETA',
        'LSFT':'LEFTSHIFT',
        'MINS':'MINUS',
        'NLCK':'NUMLOCK',
        'P0':'KP0',
        'P1':'KP1',
        'P2':'KP2',
        'P3':'KP3',
        'P4':'KP4',
        'P5':'KP5',
        'P6':'KP6',
        'P7':'KP7',
        'P8':'KP8',
        'P9':'KP9',
        'PAST':'KPASTERISK',
        'PDOT':'KPDOT',
        'PENT':'KPENTER',
        'PGDN':'PAGEDOWN',
        'PGUP':'PAGEUP',
        'PMNS':'KPMINUS',
        'PPLS':'KPPLUS',
        'PSCR':'SYSRQ',#'PRINT', # not sure?
        'PSLS':'KPSLASH',
        'QUOT':'APOSTROPHE',
        'RALT':'RIGHTALT',
        'RBRC':'RIGHTBRACE',
        'RCTL':'RIGHTCTRL',
        'RGHT':'RIGHT',
        'RGUI':'RIGHTMETA',
        'RSFT':'RIGHTSHIFT',
        'SCLN':'SEMICOLON',
        'SLCK':'SCROLLLOCK',
        'SLSH':'SLASH',
        'SPC':'SPACE',
    }
    keymap_list = []
    for keymap in keymaps:
        key_list = []
        keymap_list.append(key_list)
        for key in keymap.split(','):
            key = key.strip()
            new_key = 'KEY_'+short_to_long.get(key, key)
            if args.dump and new_key not in event_keys[1]: # todo: probably should exit with some helpful error here?
                #print 'Key', key, 'does not exist!'
                #print "'", key, "':'',"
                print "'%s':''," % key
            key_list.append(new_key)

    #pprint.pprint(keymap_list)
    #exit(0)
    mykeymaps = []
    default_keymap = keymap_list[0]
    keymap_range = range(0, len(default_keymap))
    from array import array
    for keymap in keymap_list:
        mykeymap = {}
        mykeymaps.append(mykeymap)
        for y in keymap_range:
            if default_keymap[y] != keymap[y]:
                mykeymap[default_keymap[y]] = keymap[y]

    #pprint.pprint(mykeymaps)
    #exit(0)
    #print 'mykeymap: ', mykeymap
    #print 'rev_event_keys[1]: ', rev_event_keys[1]
    #print 'event_keys[1]: ', event_keys[1]
    #print 'event_keys[1]: '
    #pprint.pprint(event_keys[1])
    #exit(0)
    # convert mykeymap once, at startup, to a faster array, possibly using a little more memory
    keycnt_range = range(0, event_keys[1]['KEY_CNT'])
    runtime_keymaps = []
    for mykeymap in mykeymaps:
        mycodemap = array('H')
        runtime_keymaps.append(mycodemap)
        for x in keycnt_range:
            key = rev_event_keys[1].get(x, 'NO_KEY_EXISTS_FOR_THIS_INDEX')
            value = event_keys[1].get(mykeymap.get(key, key), x)
            mycodemap.append(value)
    #print 'mycodemap: ', mycodemap
    #pprint.pprint(runtime_keymaps)
    #exit(0)
    active_keymap_index = default_keymap_index
    revert_default_code = event_keys[1]['KEY_'+revert_default_key]
    active_keymap = runtime_keymaps[active_keymap_index]

    switch_layout_codes = {}
    for key in switch_layout_keys:
        switch_layout_codes[event_keys[1]['KEY_'+key]] = False
    switch_layout_mode = False
    num_codes_to_index = {}
    for x in range(0, len(runtime_keymaps)):
        num_codes_to_index[event_keys[1].get('KEY_'+str(x))] = x
    #pprint.pprint(num_codes_to_index)
    #exit(0)

    return runtime_keymaps, active_keymap_index, revert_keymap_index, active_keymap, revert_default_code, switch_layout_codes, switch_layout_mode, num_codes_to_index
