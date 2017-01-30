#!/usr/bin/python3

from time import sleep
import sys

morse_dict = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '.': '.-.-.-',   #<AAA>
    ',': '--..--',   #<MIM>
    '?': '..--..',   #<IMI>
    '/': '-..-.',    #<DN>
    '+': '.-.-.',    #<AR> End of Message
    '*': '...-.-',   #<SK> End of Work
    '=': '-...-',    #<BT>
    ';': '-.-.-.',   #<KR>
    ':': '---...',   #<OS>
    "'": '.----.',   #<WG>
    '"': '.-..-.',   #<AF>
    '-': '-....-',   #<DU>
    '_': '..--.-',   #<IQ>
    '$': '...-..-',  #<SX>
    '(': '-.--.',    #<KN>
    ')': '-.--.-',   #<KK>
    '&': '.-...',    #<AS> Wait
    '!': '...-.',    #<SN> Understood
    '%': '-.-.-',    #<KA> Starting Signal
    '@': '........', #<HH> Error
    '#': '.-.-..',   #<AL> Paragraph
    }

DELAY_INTRA_SECS = 1  # Pause between two pulses (dot/dash) in seconds
DELAY_INTER_SECS = 3  # Pause between two characters in seconds)

FREQ = 800
DELAY_DOT_MILLIS = 250
DELAY_DASH_MILLIS = 1000

IR_PIN = 23

ON_PI = False
if sys.platform.startswith("linux"):
    ON_PI = True

visual = False
audio = False
IR = False

if ON_PI:
    try:
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(IR_PIN, GPIO.OUT)
        audio = False
        IR = True
    except RuntimeError:
        print("Error importing RPi.GPIO! ")
else:
    import winsound
    audio = True
    IR = False

def ir_beep(delay):
    GPIO.output(IR_PIN, GPIO.LOW)
    GPIO.output(IR_PIN, GPIO.HIGH)
    sleep(delay/1000)
    GPIO.output(IR_PIN, GPIO.LOW)
    return

def emit_dot():
    if visual:
        print ('.', end="", flush=True)
    if audio:
        winsound.Beep(FREQ, DELAY_DOT_MILLIS)
    if IR:
        ir_beep(DELAY_DOT_MILLIS)
    sleep(DELAY_INTRA_SECS)

def emit_dash():
    if visual:
        print('-', end="", flush=True)
    if audio:
        winsound.Beep(FREQ, DELAY_DASH_MILLIS)
    if IR:
        ir_beep(DELAY_DASH_MILLIS)
    sleep(DELAY_INTRA_SECS)

def emit_blank():
    if visual:
        print(' ', end="", flush=True)
    sleep(DELAY_INTER_SECS)

def emit_character(c):
    c = c.upper()
    if c not in morse_dict:
        return

    for pulse in morse_dict[c]:
        if pulse == '-':
            emit_dash()
        else:
            emit_dot()

    sleep(DELAY_INTER_SECS)


# MAIN LOOP
emitter_string = "Hello world!"

emit_character('%') # Starting signal

for c in emitter_string:
    emit_character(c)

emit_character('+') # end of message

if IR:
    GPIO.cleanup()
