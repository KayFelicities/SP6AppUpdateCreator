"""
sp6 merge
"""
import os
import sys
import getopt
import configparser
import traceback
import time
import hashcalc

VERSION = 'V0.1'
DATE = '20180601'

TEMP_PATH = os.path.join(os.environ["TMP"], str(time.time()).split('.')[0])
WORKING_PATH = None
SOFTWARE_PATH = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0])
SOFTWARE_REAL_PATH = sys._MEIPASS if getattr(sys, 'frozen', False) else SOFTWARE_PATH
CONFIG_FILE = os.path.join(SOFTWARE_PATH, r'appupdate.ini')
CONFIG_FILE_CONTENT_DEFAULT =\
r'''[outfile]
path = update.img

'''

UPDATE_SCRIPT_FORMAT =\
'''#!/bin/sh

killall -9 sxDaemon
killall -9 sxConsole
killall -9 sxShell
killall -9 sp6
killall -9 sxChan
killall -9 mosquitto

array_file="%s"
load_path="/media/app/bin"
for name in ${array_file};do
 cp /mnt/update/${name} ${load_path}
 chmod +x ${load_path}/${name}
 echo ${load_path}/${name}
done

wdt &

cd ${load_path}
rm bin.md5
md5sum * > bin.md5
sync
reboot
'''

class ConfigClass():
    """merge config"""
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            print('config file not found, create new.')
            with open(CONFIG_FILE, 'w', encoding='utf-8') as new_file:
                new_file.write(CONFIG_FILE_CONTENT_DEFAULT)
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE, encoding='utf-8-sig')

    def chk_config(self):
        """chk config"""
        if not self.outfile_cfg().get('path'):
            raise Exception('out file invalid, merge abort.')

    def outfile_cfg(self):
        """outfile_cfg"""
        return self.config['outfile']

CONFIG = ConfigClass()


def create_img(outpath):
    """main"""
    try:
        sh_file_path = os.path.join(WORKING_PATH, 'autorun.sh')
        md5_file_path = os.path.join(WORKING_PATH, 'bin.md5')
        if os.path.isfile(sh_file_path):
            os.remove(sh_file_path)
        if os.path.isfile(md5_file_path):
            os.remove(md5_file_path)

        dos2unix_path = os.path.join(SOFTWARE_REAL_PATH, r'mkcramfs\dos2unix.exe')

        # write script
        files = ['%s'%x for x in os.listdir(WORKING_PATH) if os.path.isfile(os.path.join(WORKING_PATH, x))]
        sh_content = UPDATE_SCRIPT_FORMAT%(' '.join(files))
        with open(sh_file_path, 'w') as sh_file:
            sh_file.write(sh_content)
        os.system(dos2unix_path + ' "' + sh_file_path + '"')

        # calc md5
        md5_content = hashcalc.md5sum(WORKING_PATH)
        with open(md5_file_path, 'w') as md5_file:
            md5_file.write(md5_content)
        os.system(dos2unix_path + ' "' + md5_file_path + '"')

        # mk cramfs
        mkcramfs_path = os.path.join(SOFTWARE_REAL_PATH, r'mkcramfs\mkcramfs.exe')
        cmd = mkcramfs_path + ' "' + WORKING_PATH + '" "' + outpath + '"'
        print('cmd:', cmd)
        if os.system(cmd) != 0:
            raise Exception('mkcramfs error, merge abort.')
        return 0
    except Exception:
        traceback.print_exc()
        return -1
    finally:
        # del sh
        if os.path.isfile(sh_file_path):os.remove(sh_file_path)
        # if os.path.isfile(md5_file_path):os.remove(md5_file_path)


def del_outfile(outpath):
    """delete outfile"""
    try:
        if os.path.isfile(outpath):
            os.remove(outpath)
    except Exception:
        traceback.print_exc()
        print('outfile del failed.')

if __name__ == '__main__':
    try:
        CONFIG.chk_config()
        opts, args = getopt.getopt(sys.argv[1:], "o:")
        if not args:
            raise Exception('ERROR: 请将需要打包的文件夹拖到本软件上进行打包')
        WORKING_PATH = args[0]
        out_file_path = os.path.join(WORKING_PATH, '..', CONFIG.outfile_cfg().get('path'))
        for op, value in opts:
            if op == '-o':
                out_file_path = os.path.join(value)
        if not os.path.isdir(WORKING_PATH):
            raise Exception('ERROR: working path{path} invalid.'.format(path=WORKING_PATH))

        tm_start = time.time()
        print('SP6 App Update Creator {ver}({date}).Designed by Kay.'.format(ver=VERSION, date=DATE))
        print('WORKING_PATH:', WORKING_PATH)
        print('CONFIG_FILE:', CONFIG_FILE)
        print('out file:', out_file_path)

        if create_img(out_file_path) == 0:
            print('success')
        else:
            raise Exception('!!FAILED!!')
        print('time use {tm:.1f}s'.format(tm=time.time() - tm_start))
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        os.system('color 47')
        del_outfile(out_file_path)
        time.sleep(3)
        os.system('color 07')
        sys.exit(1)

