# web-app.spec (Final, Definitive Version)
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_dynamic_libs

# --- Platform-Specific Configuration ---
use_upx = sys.platform != 'darwin'

block_cipher = None

a = Analysis(
    ['webapp/app.py'],
    binaries=collect_dynamic_libs('python'),
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    hiddenimports=['waitress']
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pi-selfhosting-web',
    console=False,
    upx=use_upx, # Use our platform-aware variable
    version='file_version_info.txt'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=use_upx, # Use our platform-aware variable
    upx_exclude=[],
    name='pi-selfhosting-web'
)
