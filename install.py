import os
import wget

print('欢迎使用Tsukiko部署程序')
print('本程序默认您的系统为Windows64位。若不具备以上条件请自行部署')
print('正在下载Wget...')
wget.download('https://eternallybored.org/misc/wget/1.20.3/64/wget.exe')
app_is_installed = input('您是否已经安装Python，Pip，Git？(Y/N):').upper()
if app_is_installed == 'N':
    print('正在下载Git...')
    os.system('')
    print('正在安装...若弹出窗口请一路Next')
    os.system(
        'wget -o git.exe https://www.gitclone.com/download/Git-2.29.2-64-bit.exe')
    print('正在下载Python...')
    os.system(
        'wget -o python.exe https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe')
    print('正在安装...若弹出窗口请一路Next')
    os.system('python.exe')
    print('正在安装Pip...')
    os.system('wget -o get-pip.py https://bootstrap.pypa.io/get-pip.py')
    os.system('python get-pip.py')
print('正在下载Mirua...')
os.system('wget https://cdn.jsdelivr.net/gh/zkonge/mirua-update@master/v0.1.2/mirua_windows_x86_64')
os.rename('mirua_windows_x86_64', 'mirua.exe')
print('正在部署Mirai...')
os.system('mirua.exe')
print('正在下载Tsukiko...')
os.system('git clone https://github.com/umauc/Tsukiko.git')
print('正在安装Tsukiko依赖')
os.system('pip install -r Tsukiko/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple')
print('部署成功！')
