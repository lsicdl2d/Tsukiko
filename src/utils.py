from .uconomy import Uconomy
from .user import User
from decimal import Decimal
from config.bot_config import regiser_reward
from .exception import IllegalSteamIdError,BalanceNotEnoughError,IllggalCommandFormatError
from graia.application.message.elements.internal import At,Plain

uconomy = Uconomy()
user = User()

def regiser(text,qid):
    steamid = text.replace('#注册','').replace(' ','')
    if steamid.isdigit() and len(steamid) == 17:
        user.userInit(qid=qid,steamid=steamid)
        user_balance = uconomy.getUserBalance(steamid)
        uconomy.setUserBalance(steamid,user_balance + Decimal(regiser_reward))
    else:
        raise IllegalSteamIdError

def transfer(msgchain,qid):
    try:
        other_side_steamid = user.getSteamId(msgchain.get(At)[0].target)
        main_side_steamid = user.getSteamId(qid)
        transfer_balance = Decimal(int(msgchain.get(Plain)[1].text))
        if uconomy.getUserBalance(main_side_steamid) >= transfer_balance:
            uconomy.setUserBalance(main_side_steamid,uconomy.getUserBalance(main_side_steamid)-transfer_balance)
            uconomy.setUserBalance(other_side_steamid,uconomy.getUserBalance(other_side_steamid)+transfer_balance)
        else:
            raise BalanceNotEnoughError
    except IndexError:
        raise IllggalCommandFormatError
