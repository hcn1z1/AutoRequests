
class CustomException(Exception):
    pass

class UnsuccessfulRequestError(CustomException):
    def __init__(self, message = "Unsuccessful Request, couldn't check all success values. Maybe change them or add more layers") -> None:
        self.message = message
        super().__init__(self.message)

class BadConfigError(CustomException):
    def __init__(self, message = "Error loading data from config. Bad Config or File doesn't exist.", path = "",keys = ()) -> None:
        self.message = message
        self.message += f"\n{path} => "
        self.message = self.message + str(keys) if keys != () else message
        super().__init__(self.message)

class LoadDriverError(CustomException):
    def __init__(self, message = "Couldn't load config error, (for more informations : https://playwright.dev/python/docs/intro)") -> None:
        self.message = message
        super().__init__(self.message)