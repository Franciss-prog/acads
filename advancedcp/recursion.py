import time
import os


def timebomb(seconds):

    # end case
    if seconds == 0:
        print("BOOM!")
        return
    print(seconds)
    time.sleep(1)
    os.system("clear")
    timebomb(seconds - 1)


timebomb(10)
