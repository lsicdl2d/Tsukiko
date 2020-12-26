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
from config.bot_config import mirai_account,mirai_authKey,mirai_host,signin_command,regiser_command,regiser_success_msg,user_already_have_msg,user_already_signin_msg,user_not_found_msg,user_not_login_msg,info_command,regiser_reward
from src.user import User
from src.uconomy import Uconomy
from src.uconomy import Shop
from templates.templates import Signin as Signin_template, Userinfo
from templates.templates import Userinfo as Userinfo_template

loop = asyncio.get_event_loop()
user = User()
shop = Shop()
uconomy = Uconomy()
signin = Signin()
Signin = Signin_template()
Userinfo = Userinfo_template()

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


async def FastSender(group, qid, text):
    await app.sendGroupMessage(group, MessageChain.create([At(target=qid), Plain(text=text)]))

@bcc.receiver("GroupMessage")
async def MessageHanler(app: GraiaMiraiApplication,group:Group,member:Member,msg:MessageChain):
    if msg.has(Plain):
        text = msg.get(Plain)[0].text
        try:
            if text == info_command:
                await FastSender(group,member.id,Userinfo.templatesBuild(steamid=user.getSteamId(member.id)))
            elif text.find(regiser_command) != -1:
                steamid = text.replace('#注册','').replace(' ','')
                if steamid.isdigit() and len(steamid) == 17:
                    user.userInit(qid=member.id,steamid=steamid)
                    user_balance = uconomy.getUserBalance(steamid)
                    uconomy.setUserBalance(steamid,user_balance + Decimal(regiser_reward))
                    await FastSender(group,member.id,regiser_success_msg)
            elif text == signin_command:
                signin.signin(member.id)
                await FastSender(group,member.id,Signin.templatesBuild(qid=member.id))
        except UserNotFoundError:
            await FastSender(group, member.id, user_not_found_msg)
        except UserNotLoginError:
            await FastSender(group, member.id, user_not_login_msg)
        except UserAlreadyHaveError:
            await FastSender(group,member.id,user_already_have_msg)
        except UserAlreadySigninTodayError:
            await FastSender(group,member.id,user_already_signin_msg)


@scheduler.schedule(crontabify("0 4 * * * *"))
def clear_signin_data():
    signin.clearTodaySignin()

loop.run_forever()
app.launch_blocking()
