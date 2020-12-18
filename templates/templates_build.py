from src.uconomy import uconomy,shop
from src.rank import rank
from decimal import Decimal
from src.signin import signin

uconomy = uconomy()
shop = shop()
rank = rank()
signin = signin()

def templates_build(mode,**var_dict):
    if mode == 'userinfo':
        steamid = var_dict.get('steamid')
        template = open('./templates/用户详情.txt','r').read()
        for i,j in [
            ('!GAMENAME',rank.get_user_rank_info(steamid).get('lastDisplayName')),
            ('!STEAMID',steamid),
            ('!BALANCE', Decimal.to_eng_string(uconomy.get_user_balance(steamid))),
            ('!RANK', str(rank.get_user_rank_info(steamid).get('points')))
        ]:
            template = template.replace(i,j)
        return template
    elif mode == 'signin':
        qid = var_dict.get('qid')
        template = open('./templates/签到.txt','r').read()
        for i,j in [
            ('!REWARD', Decimal.to_eng_string(signin.get_lastReward(qid))),
            ('!CONTINUED', str(signin.get_continued_signin(qid))),
            ('!TOTAL', str(signin.get_total_signin(qid)))
        ]:
            template = template.replace(i,j)
        return template

