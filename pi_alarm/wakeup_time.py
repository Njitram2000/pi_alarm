class WakeupTime:
    def __init__(self, hours: int, minutes: int) -> None:
        self.__hours = hours
        self.__minutes = minutes
    
    @property
    def hours(self):
        return self.__hours

    @property
    def minutes(self):
        return self.__minutes