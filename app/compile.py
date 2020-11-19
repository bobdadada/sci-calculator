import os
import sys
import shutil
from config import *

os.environ['PATH'] = path

dst = dstdir + name + '.exe'

exestr = 'pyinstaller -F --clean ' + ' -w {}.py'.format(src_name) + ' -i {}'.format(icon)
print(exestr)

# 当发生RecursionError时添加的补丁
patch = """
import sys
sys.setrecursionlimit(100000)
"""
patch = [p.strip() + '\n' for p in patch.split('\n')]

# 子程序返回值
r = os.system(exestr)

if r:
    print('error happened when using pyinstaller, try set larger maximum recursion depth.')
    file = '{}.spec'.format(src_name)
    tempfile = '_' + file
    with open(file, 'r') as fp, open(tempfile, 'w') as gp:
        lines = fp.readlines()
        lines = lines[0:2] + patch + lines[1:]
        gp.writelines(lines)
    os.remove(file)
    os.rename(tempfile, file)
    exestr = 'pyinstaller {}'.format(file)
    print(exestr)
    r = os.system(exestr)

if r:
    print('error happened when using pyinstaller')
else:
    if not os.path.isdir(dstdir):
        os.mkdir(dstdir)
    if os.path.isfile(dst):
        os.remove(dst)
    print('save to %s.' % dst)
    shutil.copy('./dist/{}.exe'.format(src_name), dst)
