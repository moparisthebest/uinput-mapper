#!/bin/bash

kbs=''
for input in $(ls /dev/input/event*)
do
        if udevadm info -q property $input | grep ID_INPUT_KEYBOARD
        then
                udevadm info -a $input | grep 'keymapper input device' || kbs="$kbs $input"
        fi
done

exec /usr/bin/env python2 /usr/lib/uinput-mapper/input-read -d -k /etc/uinput-mapper/keymap.py $kbs
