from templates.templates import ItemSearch, VehicleSearch
from .uconomy import Shop, Uconomy
from .user import User
from decimal import Decimal
from config.bot_config import (register_reward, register_command, search_item_command, 
                                search_vehicle_command, get_shop_item_info_command,get_shop_vehicle_info_command,
                                item_not_found_msg,vehicle_not_found_msg,set_shop_item_info_command,
                                set_shop_vehicle_info_command, parameter_separator)
from .exception import IllegalSteamIdError,BalanceNotEnoughError,IllegalCommandFormatError, ItemNotFoundError,ValueIsNegativeError, VehicleNotFoundError
from graia.application.message.elements.internal import At,Plain
from graia.application.message.chain import MessageChain

uconomy = Uconomy()
user = User()
shop = Shop()
ItemSearch = ItemSearch()
VehicleSearch = VehicleSearch()

def register(text: str,qid: str):
    steamid = text.replace(register_command,'').replace(' ','')
    if steamid.isdigit() and len(steamid) == 17:
        user.userInit(qid=qid,steamid=steamid)
        user_balance = uconomy.getUserBalance(steamid)
        uconomy.setUserBalance(steamid,user_balance + Decimal(register_reward))
    else:
        raise IllegalSteamIdError

def transfer(msgchain: MessageChain,qid: str):
    try:
        other_side_steamid = user.getSteamId(msgchain.get(At)[0].target)
        main_side_steamid = user.getSteamId(qid)
        transfer_balance = Decimal(int(msgchain.get(Plain)[1].text))
        if transfer_balance <= Decimal(0):
            raise ValueIsNegativeError
        else:
            if uconomy.getUserBalance(main_side_steamid) >= transfer_balance:
                uconomy.setUserBalance(main_side_steamid,uconomy.getUserBalance(main_side_steamid)-transfer_balance)
                uconomy.setUserBalance(other_side_steamid,uconomy.getUserBalance(other_side_steamid)+transfer_balance)
            else:
                raise BalanceNotEnoughError
    except IndexError:
        raise IllegalCommandFormatError

def recharge(msgchain: MessageChain,qid: str):
    try:
        if user.checkUserPermission(qid,1):
            other_side_steamid = user.getSteamId(msgchain.get(At)[0].target)
            recharge_balance = Decimal(int(msgchain.get(Plain)[1].text))
            uconomy.setUserBalance(other_side_steamid,uconomy.getUserBalance(other_side_steamid)+recharge_balance)
        else:
            raise PermissionError
    except IndexError:
        raise IllegalCommandFormatError

def item_search(text: str)-> str:
    itemname = text.replace(search_item_command,'').replace(' ','')
    return ItemSearch.templatesBuild(shop.searchShopItem(itemname))

def vehicle_search(text: str) -> str:
    vehiclename = text.replace(search_vehicle_command, '').replace(' ', '')
    return VehicleSearch.templatesBuild(shop.searchShopVehicle(vehiclename))

def shop_item_get(text: str)-> str:
    try:
        return ItemSearch.templatesBuild([shop.getShopItemInfo(text.replace(get_shop_item_info_command,'').replace(' ',''))])
    except IndexError:
        raise ItemNotFoundError

def shop_vehicle_get(text: str)-> str:
    try:
        return VehicleSearch.templatesBuild([shop.getShopVehicleInfo(text.replace(get_shop_vehicle_info_command, '').replace(' ', ''))])
    except IndexError:
        raise VehicleNotFoundError

def shop_item_set(text: str,qid: str):
    if user.checkUserPermission(qid,1):
        arg = text.replace(set_shop_item_info_command,'').replace(' ','').split(parameter_separator)
        shop.setShopItem(itemid=arg[0],itemname=arg[1],cost=arg[2],buyback=arg[3])
    else:
        raise PermissionError

def shop_vehicle_set(text: str,qid: str):
    if user.checkUserPermission(qid,1):
        arg = text.replace(set_shop_vehicle_info_command,'').replace(' ','').split(parameter_separator)
        shop.setShopVehicle(vehicleid=arg[0],vehiclename=arg[1],cost=arg[2],buyback=arg[3])
    else:
        raise PermissionError

def set_permission(msgchain:MessageChain,qid:str):
    try:
        if user.checkUser(qid):
            user.setUserPermission(str(msgChain.get(At)[0].target), int(msgChain.get(Plain)[0].text))
        else:
            raise PermissionError
    except IndexError:
        raise IllegalCommandFormatError