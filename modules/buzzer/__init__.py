import time
from thread import start_new_thread
from modules import cbpi

try:
    import RPi.GPIO as GPIO
except Exception as e:
    pass

class Buzzer(object):

    sound = ["H", 0.1, "L"]
    def __init__(self, gpio):
        try:
            cbpi.app.logger.info("INIT BUZZER NOW GPIO%s" % gpio)
            self.gpio = gpio
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio, GPIO.OUT)
            self.state = True
            cbpi.app.logger.info("BUZZER SETUP OK")
        except Exception as e:
            self.state = False

    def beep(self):
        if self.state is False:
            cbpi.app.logger.error("BUZZER not working")
            return

        def play(sound):
            try:
                for i in sound:
                    if (isinstance(i, str)):
                        if i == "H":
                            GPIO.output(int(self.gpio), GPIO.HIGH)
                        else:
                            GPIO.output(int(self.gpio), GPIO.LOW)
                    else:
                        time.sleep(i)
            except Exception as e:
                pass

        start_new_thread(play, (self.sound,))

@cbpi.initalizer(order=0)
def init(cbpi):
    print "INIT BUZZER"
    cbpi.app.logger.info("INIT BUZZER")
    gpio = cbpi.get_config_parameter("buzzer", 16)
    cbpi.buzzer = Buzzer(gpio)
    cbpi.beep()
    cbpi.app.logger.info("INIT OK")
