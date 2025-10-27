def make_it_speak(obj):
    if hasattr(obj, "speak"):
        obj.speak()
    else:
        print("This object cannot speak!")


class Bird:
    def speak(self):
        print("Chirp!")


class Robot:
    def speak(self):
        print("Beep!")


# Test
make_it_speak(Bird())
make_it_speak(Robot())
make_it_speak(123)  # prints warning
