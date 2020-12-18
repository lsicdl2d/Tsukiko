class UserNotFoundError(Exception):
    pass


class UserAlreadyHaveError(Exception):
    pass


class UserNotLoginError(Exception):
    pass


class UserAlreadySigninTodayError(Exception):
    pass

class IllegalSteamId(Exception):
    pass