# web-app.spec (Final, Definitive Version)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs
import sys

block_cipher = None
binaries = []

a = Analysis(
    ['webapp/app.py'],
    binaries=binaries,
    # Ensure these paths are correct for your project structure
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    hiddenimports=['waitress']
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='pi-selfhosting-web',
    # This should be False for a web/GUI application to hide the console
    console=False,
    upx=True,
    version='file_version_info.txt',
    onefile=True
)
