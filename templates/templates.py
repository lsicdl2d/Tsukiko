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
    def templatesBuild(self,steamid: str) -> str:
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
    def templatesBuild(self,qid: str) -> str:
        template = open('./templates/签到.txt','r').read()
        for i,j in [
            ('!REWARD', Decimal.to_eng_string(signin_module.getLastReward(qid))),
            ('!CONTINUED', str(signin_module.getContinuedSignin(qid))),
            ('!TOTAL', str(signin_module.getTotalSignin(qid)))
        ]:
            template = template.replace(i,j)
        return template

class ItemSearch(Template):
    def templatesBuild(self,itemsearchresult: list) -> str:
        template = open('./templates/物品搜索.txt','r').read()
        template_list = template.splitlines()
        for i in template_list:
            if i.startswith('$'):
                template.replace(i,f"{i}'\n'"*len(itemsearchresult))
        template_list = template.splitlines()
        new_template = ''
        for i in template_list:
            if i.startswith('$'):
                loop_line = i.replace('$','')
                template = template.replace(i,'$WAITFORREPLACE')
        for l in range(len(itemsearchresult)):
            replaced_line = loop_line
            for j,k in [
                ('!ID',itemsearchresult[l]['id']),
                ('!ITEMNAME',itemsearchresult[l]['itemname']),
                ('!COST',itemsearchresult[l]['cost']),
                ('!BUYBACK',itemsearchresult[l]['buyback'])
            ]:
                replaced_line = replaced_line.replace(j,k)
            new_template = new_template+replaced_line+'\n'
        return template.replace('$WAITFORREPLACE',new_template)

class VehicleSearch(Template):
    def templatesBuild(self, vehiclesearchresult: list) -> str:
        template = open('./templates/载具搜索.txt', 'r').read()
        template_list = template.splitlines()
        for i in template_list:
            if i.startswith('$'):
                template.replace(i, f"{i}'\n'"*len(vehiclesearchresult))
        template_list = template.splitlines()
        new_template = ''
        for i in template_list:
            if i.startswith('$'):
                loop_line = i.replace('$', '')
                template = template.replace(i, '$WAITFORREPLACE')
        for l in range(len(vehiclesearchresult)):
            replaced_line = loop_line
            for j, k in [
                ('!ID', vehiclesearchresult[l]['id']),
                ('!VEHICLENAME', vehiclesearchresult[l]['vehiclename']),
                ('!COST', vehiclesearchresult[l]['cost']),
            ]:
                replaced_line = replaced_line.replace(j, k)
            new_template = new_template+replaced_line+'\n'
        return template.replace('$WAITFORREPLACE', new_template)
