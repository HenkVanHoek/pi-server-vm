# web-app.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

import sys
binaries_list = []
if sys.platform == 'win32':
    from PyInstaller.utils.hooks import collect_dynamic_libs
    binaries_list = collect_dynamic_libs('python')

a = Analysis(
    ['webapp/app.py'],
    binaries=binaries_list,
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    hiddenimports=['waitress'],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='pi-selfhosting-web',
    console=True,
    upx=True,
    # Point directly to the version info file.
    version='file_version_info.txt'
)
