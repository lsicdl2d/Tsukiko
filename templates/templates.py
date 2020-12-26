from src.uconomy import Uconomy,Shop
from src.rank import Rank
from decimal import Decimal
from src.signin import Signin as signin_module

uconomy = Uconomy()
shop = Shop()
rank = Rank()
signin_module = signin_module()

class Template(object):
    def templatesBuild(self):
        pass

class Userinfo(Template):
    def templatesBuild(self,steamid):
        template = open('./templates/用户详情.txt', 'r').read()
        for i, j in [
            ('!GAMENAME', rank.getUserRankInfo(steamid).get('lastDisplayName')),
            ('!STEAMID', steamid),
            ('!BALANCE', Decimal.to_eng_string(uconomy.getUserBalance(steamid))),
            ('!RANK', str(rank.getUserRankInfo(steamid).get('points')))
        ]:
            template = template.replace(i, j)
        return template

class Signin(Template):
    def templatesBuild(self,qid):
        template = open('./templates/签到.txt','r').read()
        for i,j in [
            ('!REWARD', Decimal.to_eng_string(signin_module.getLastReward(qid))),
            ('!CONTINUED', str(signin_module.getContinuedSignin(qid))),
            ('!TOTAL', str(signin_module.getTotalSignin(qid)))
        ]:
            template = template.replace(i,j)
        return template

