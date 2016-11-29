#!/bin/bash
inotifywait -m -q -e create -e delete --include '.*event[0-9]+' --format '%e-%w%f' /dev/input/ | while read event
do

# CREATE-/dev/input/event16
if echo "$event" | grep '^CREATE-'
then
	input="$(echo "$event" | sed 's/^CREATE-//')"
	# if it's us, ignore
	udevadm info -a "$input" | grep 'keymapper input device' && continue	
	# if it's not a keyboard, ignore
	udevadm info -q property "$input" | grep ID_INPUT_KEYBOARD || continue
fi 

systemctl restart dvorak
done
