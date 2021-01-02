from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from decimal import Decimal
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify

from graia.application.message.elements.internal import Plain, At
from graia.application.group import Group, Member

from src.signin import Signin
from src.exception import *
from config.bot_config import mirai_account,mirai_authKey,mirai_host
from config.bot_config import transfer_command,signin_command,register_command,info_command,search_item_command,search_vehicle_command,recharge_command
from config.bot_config import permission_not_enough_msg, illegal_steamid_msg, register_success_msg, user_already_have_msg, user_already_signin_msg, user_not_found_msg, user_not_login_msg, illegal_command_format_msg, balance_not_enough_msg, transfer_success_msg, item_not_found_msg, vehicle_not_found_msg, value_is_negative_msg, recharge_success_msg
from config.bot_config import signin_clear_time
from src.user import User
from plugins.plugin import Plugin
from src.uconomy import Uconomy
from src.uconomy import Shop
from templates.templates import Signin as Signin_template
from templates.templates import Userinfo as Userinfo_template
from src.utils import item_search, recharge, register,transfer, vehicle_search
from plugins.plugin import Plugin

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
        open('.botinit','r')
    except:
        print('检测到您第一次使用本插件，正在初始化...')
        user.userDatabaseInit()
        signin.signinDatabaseInit()
        with open('.botinit','w') as i:
            i.write('init')
            i.close

async def FastSender(group, qid, text):
    await app.sendGroupMessage(group, MessageChain.create([At(target=qid), Plain(text=text)]))

@bcc.receiver("GroupMessage")
async def MessageHandler(app: GraiaMiraiApplication,group:Group,member:Member,msg:MessageChain):
    if msg.has(Plain):
        text = str(msg.get(Plain)[0].text)
        qid = str(member.id)
        try:
            if text == info_command:
                await FastSender(group,qid,Userinfo.templatesBuild(steamid=user.getSteamId(member.id)))
            elif text.startswith(register_command):
                register(text,qid)
                await FastSender(group, qid, register_success_msg)
            elif text == signin_command:
                signin.signin(qid)
                await FastSender(group,qid,Signin.templatesBuild(qid=member.id))
            elif text.startswith(transfer_command):
                transfer(msg,member.id)
                await FastSender(group,qid,transfer_success_msg)
            elif text.startswith(search_item_command):
                await FastSender(group,qid,item_search(text))
            elif text.startswith(search_vehicle_command):
                await FastSender(group,qid,vehicle_search(text))
            elif text.startswith(recharge_command):
                recharge(msg,qid)
                await FastSender(group,qid,recharge_success_msg)
            else:
                plugin.runPlugin(app=app,group=group,member=member,msgChain=msg)
        except UserNotFoundError:
            await FastSender(group, member.id, user_not_found_msg)
        except UserNotLoginError:
            await FastSender(group, member.id, user_not_login_msg)
        except UserAlreadyHaveError:
            await FastSender(group,member.id,user_already_have_msg)
        except UserAlreadySigninTodayError:
            await FastSender(group,member.id,user_already_signin_msg)
        except IllegalSteamIdError:
            await FastSender(group, member.id, illegal_steamid_msg)
        except IllegalCommandFormatError:
            await FastSender(group,member.id,illegal_command_format_msg)
        except BalanceNotEnoughError:
            await FastSender(group,member.id,balance_not_enough_msg)
        except ItemNotFoundError:
            await FastSender(group, member.id, item_not_found_msg)
        except VehicleNotFoundError:
            await FastSender(group, member.id, vehicle_not_found_msg)
        except ValueIsNegativeError:
            await FastSender(group, member.id, value_is_negative_msg)
        except PermissionError:
            await FastSender(group, member.id, permission_not_enough_msg)

@scheduler.schedule(crontabify(signin_clear_time))
def clear_signin_data():
    signin.clearTodaySignin()

if __name__ == "__main__":
    check_init()
    app.launch_blocking()
