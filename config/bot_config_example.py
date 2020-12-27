#数据库设置
mysql_host = '127.0.0.1'
mysql_user = 'unturned'
mysql_password = '1234567890'
mysql_db = 'unturned'
mysql_charset = 'utf8'
mysql_uconomy_table = 'uconomy'
mysql_uconomy_shop_item_table = 'uconomyitemshop'
mysql_uconomy_shop_vehice_table = 'uconomyvehicleshop'
mysql_rank_table = 'ranks'
#签到设置
signin_max_get_balance = 1000
signin_min_get_balance = 500
signin_continued_reward = 3000
signin_continued_reward_day = 7
signin_clear_time = "0 4 * * * *"
#用户注册设置
regiser_reward = 3000
#Mirai设置
mirai_host = 'http://120.79.196.188:8080'
mirai_authKey = '1234567890'
mirai_account = 1234567890
#命令设置
info_command = '#信息查询'
regiser_command = '#注册'
signin_command = '#签到'
transfer_command = '#转账'
#消息设置
user_already_have_msg = '您已注册！'
user_not_login_msg = '此用户未进入过游戏！'
user_not_found_msg = '此用户未注册！'
regiser_success_msg = f'注册成功！开户奖励{str(regiser_reward)}已到账！'
user_already_signin_msg = '您今日已签到过了！'
illegal_steamid_msg = 'SteamID不正确！'
illegal_command_format_msg = '命令格式不正确！'
balance_not_enough_msg = '您的余额不足以完成此次操作！'
transfer_success_msg = '转账成功！'
