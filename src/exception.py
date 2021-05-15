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


class IllegalCommandFormatError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class VehicleNotFoundError(Exception):
    pass


class ValueIsNegativeError(Exception):
    pass


class CannotTransferToSelfError(Exception):
    pass
