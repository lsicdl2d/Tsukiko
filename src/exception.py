class UserNotFoundError(Exception):
    pass


class UserAlreadyHaveError(Exception):
    pass

class UserNotLoginError(Exception):
    pass

class UserAlreadySigninTodayError(Exception):
    pass

class IllegalSteamIdError(Exception):
    pass

class BalanceNotEnoughError(Exception):
    pass

class IllggalCommandFormatError(Exception):
    pass
