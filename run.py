import asyncio

from graia.application import GraiaMiraiApplication, Session
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.broadcast import Broadcast
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

from config.bot_config import mirai_account, mirai_authKey, mirai_host, admin_qq
from config.bot_config import permission_not_enough_msg, illegal_steamid_msg, register_success_msg, \
    user_already_have_msg, user_already_signin_msg, user_not_found_msg, user_not_login_msg, illegal_command_format_msg, \
    balance_not_enough_msg, transfer_success_msg, item_not_found_msg, vehicle_not_found_msg, value_is_negative_msg, \
    recharge_success_msg, set_permission_success_msg, cannot_transfer_to_self_msg
from config.bot_config import signin_clear_time
from config.bot_config import transfer_command, signin_command, register_command, info_command, search_item_command, \
    search_vehicle_command, recharge_command, get_shop_item_info_command, get_shop_vehicle_info_command, \
    set_permission_command
from plugins.plugin import Plugin
from src.exception import *
from src.signin import Signin
from src.uconomy import Shop
from src.uconomy import Uconomy
from src.user import User
from src.utils import item_search, recharge, register, transfer, vehicle_search, shop_item_get, shop_vehicle_get, \
    set_permission
from templates.templates import Signin as Signin_template
from templates.templates import Userinfo as Userinfo_template

loop = asyncio.get_event_loop()
user = User()
shop = Shop()
uconomy = Uconomy()
signin = Signin()
Signin = Signin_template()
Userinfo = Userinfo_template()
plugin = Plugin()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=mirai_host,  # 填入 httpapi 服务运行的地址
        authKey=mirai_authKey,  # 填入 authKey
        account=mirai_account,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
scheduler = GraiaScheduler(
    loop, bcc
)
plugin.loadPlugins()


def check_init():
    try:
        open('.botinit', 'r')
    except:
        print('检测到您第一次使用本插件，正在初始化...')
        user.userDatabaseInit()
        signin.signinDatabaseInit()
        user.setUserPermission(admin_qq, 2)
        with open('.botinit', 'w') as i:
            i.write('init')
            i.close


async def fast_sender(group, qid, text):
    await app.sendGroupMessage(group, MessageChain.create([At(target=qid), Plain(text=text)]))


@bcc.receiver("GroupMessage")
async def messagehandler(app: GraiaMiraiApplication, group: Group, member: Member, msg: MessageChain):
    if msg.has(Plain):
        text = str(msg.get(Plain)[0].text).replace(' ', '')
        qid = str(member.id)
        try:
            if text == info_command:
                await fast_sender(group, qid, Userinfo.templatesBuild(steamid=user.getSteamId(str(member.id))))
            elif text.startswith(register_command):
                register(text, qid)
                await fast_sender(group, qid, register_success_msg)
            elif text == signin_command:
                signin.signin(qid)
                await fast_sender(group, qid, Signin.templatesBuild(qid=str(member.id)))
            elif text.startswith(transfer_command):
                transfer(msg, str(member.id))
                await fast_sender(group, qid, transfer_success_msg)
            elif text.startswith(search_item_command):
                await fast_sender(group, qid, item_search(text))
            elif text.startswith(search_vehicle_command):
                await fast_sender(group, qid, vehicle_search(text))
            elif text.startswith(recharge_command):
                recharge(msg, qid)
                await fast_sender(group, qid, recharge_success_msg)
            elif text.startswith(get_shop_item_info_command):
                await fast_sender(group, qid, shop_item_get(text))
            elif text.startswith(get_shop_vehicle_info_command):
                await fast_sender(group, qid, shop_vehicle_get(text))
            elif text.startswith(set_permission_command):
                set_permission(msg, qid)
                await fast_sender(group, qid, set_permission_success_msg)
            else:
                await plugin.runPlugin(app=app, group=group, member=member, msgChain=msg)
        except UserNotFoundError:
            await fast_sender(group, member.id, user_not_found_msg)
        except UserNotLoginError:
            await fast_sender(group, member.id, user_not_login_msg)
        except UserAlreadyHaveError:
            await fast_sender(group, member.id, user_already_have_msg)
        except UserAlreadySigninTodayError:
            await fast_sender(group, member.id, user_already_signin_msg)
        except IllegalSteamIdError:
            await fast_sender(group, member.id, illegal_steamid_msg)
        except IllegalCommandFormatError:
            await fast_sender(group, member.id, illegal_command_format_msg)
        except BalanceNotEnoughError:
            await fast_sender(group, member.id, balance_not_enough_msg)
        except ItemNotFoundError:
            await fast_sender(group, member.id, item_not_found_msg)
        except VehicleNotFoundError:
            await fast_sender(group, member.id, vehicle_not_found_msg)
        except ValueIsNegativeError:
            await fast_sender(group, member.id, value_is_negative_msg)
        except PermissionError:
            await fast_sender(group, member.id, permission_not_enough_msg)
        except CannotTransferToSelfError:
            await fast_sender(group, member.id, cannot_transfer_to_self_msg)


@scheduler.schedule(crontabify(signin_clear_time))
def clear_signin_data():
    signin.clearTodaySignin()


if __name__ == "__main__":
    check_init()
    app.launch_blocking()
