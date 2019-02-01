# -*- mode: python -*-

block_cipher = None


a = Analysis(['backup.py'],
             pathex=['/Users/zhupeng/Work/git/grab_huaban_board'],
             binaries=[("./bin/chrome", '.'), ('./bin/chromedriver', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='backup',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='backup.app',
             icon=None,
             info_plist={'NSHighResolutionCapable': 'True'},
             bundle_identifier=None)
