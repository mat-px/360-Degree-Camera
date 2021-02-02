
use_button=27

from gpiozero import Button
from signal import pause
from subprocess import check_call

held_for=0.0

def rls():
        global held_for
        if (held_for > 5.0):
                check_call(['/sbin/poweroff']) #poweroff if held for >5 seconds
        elif (held_for > 2.0):
                check_call(['/sbin/reboot']) #reboot if held for >5 seconds
        else:
            held_for = 0.0

def hld():
        global held_for
        held_for = max(held_for, button.held_time + button.hold_time)

button=Button(use_button, hold_time=1.0, hold_repeat=True)
button.when_held = hld
button.when_released = rls

pause()
