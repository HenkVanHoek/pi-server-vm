# web-app.spec (Final, Corrected Version)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

a = Analysis(
    ['webapp/app.py'],
    binaries=collect_dynamic_libs('python'),
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    # This is the crucial line that fixes the ModuleNotFoundError
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
    upx=True,
    version='file_version_info.txt'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pi-selfhosting-web'
)
