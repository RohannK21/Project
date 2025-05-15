import RPi.GPIO as GPIO
import time
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.', ' ': '/'
}
#GPIO_pins
LED_PIN = 18
BUZZER_PIN = 23
BUTTON_PIN = 17

#ENG_in_MORSE_out
def text_to_morse(text):
    morse_code = ''
    for char in text.upper():
        if char in morse_code_dict:
            morse_code += morse_code_dict[char] + ' '
    return morse_code.strip()

#Morse_LED_blink
def blink_morse_code(morse_code):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    for symbol in morse_code:
        if symbol == '.':
            GPIO.output(LED_PIN, GPIO.HIGH)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  #ON for dot
            time.sleep(0.2)  #duration
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)  #OFF
            time.sleep(0.2)  # Inter-element gap
        elif symbol == '-':
            GPIO.output(LED_PIN, GPIO.HIGH)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  #ON for dash
            time.sleep(0.6)  #duration
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)  #OFF
            time.sleep(0.2)  #Inter-element gap
        elif symbol == '/':
            time.sleep(0.4)  #Inter-character gap

    GPIO.cleanup()

# MORSE_in
def read_morse_input():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    input_text = ''
    prev_input_state = True
    start_time = None

    while True:
        input_state = GPIO.input(BUTTON_PIN)

        if input_state == False and prev_input_state == True:
            start_time = time.time()

        if input_state == False and prev_input_state == False:
            if time.time() - start_time > 0.5:  # Timeout for dot/dash separation
                input_text += '-'  # Dash
                print("-")
                time.sleep(0.2)  # Inter-element gap
            else:
                input_text += '.'  
                print(".")
                time.sleep(0.2)  # Inter-element gap

        if input_state == True and prev_input_state == False:
            if time.time() - start_time > 1:  # Timeout for character separation
                break

        prev_input_state = input_state

    return input_text

def main():
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    while True:
        choice = input("Choose an option:\n1. TEXTin MORSEout\n2. MORSEin TEXTout\n3. Exit\nEnter your choice: ")
        if choice == '1':
            text = input("TEXTin: ")
            morse = text_to_morse(text)
            print("MORSEout:", morse)
            blink_morse_code(morse)
        elif choice == '2':
            morse_code = read_morse_input()
            text = ''
            for symbol in morse_code.split(' '):
                for key, value in morse_code_dict.items():
                    if symbol == value:
                        text += key
            print("TEXTout:", text)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid!")

if __name__ == "__main__":
    main()
