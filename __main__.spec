# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['C:\\Users\\wangke\\Desktop\\VirtualBox\\python\\SP6AppUpdateCreator'],
             binaries=[],
             datas=[('mkcramfs\\', 'mkcramfs\\'),],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SP6AppUpdateCreator',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='logo.ico')
