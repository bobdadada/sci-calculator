import os
import sys
import shutil
from config import *

os.environ['PATH'] = path

dst = dstdir + name + '.exe'

if os.system('pyinstaller -F --clean -w {}.py'.format(name)):
    print('error happened when using pyinstaller')
else:
    if not os.path.isdir(dstdir):
        os.mkdir(dstdir)
    if os.path.isfile(dst):
        os.remove(dst)
    shutil.copy('./dist/{}.exe'.format(name), dst)
