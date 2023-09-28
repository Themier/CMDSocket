
from commands.uploadFile import makePath
from constants import *
import time
import shutil

back_path = os.path.join(prjPath, os.pardir, 'backUps')
makePath(back_path)
shutil.make_archive(os.path.join(back_path, 'updateProject_{}'.format(time.time())),'zip',prjPath)