# -*- mode: python -*-
a = Analysis(['./scripts\\..\\src\\hppserv.pyw'],
             pathex=['./scripts'],
             hiddenimports=[],
             hookspath=['./scripts\\hooks'],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hppserv.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False )
