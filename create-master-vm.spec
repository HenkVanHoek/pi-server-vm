# create-master-vm.spec (Final, Definitive Version)
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_dynamic_libs

# --- Platform-Specific Configuration ---
use_upx = sys.platform != 'darwin'

block_cipher = None

a = Analysis(
    ['run_create_master.py'],
    binaries=collect_dynamic_libs('python'),
    datas=[],
    hiddenimports=[]
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='create-master-vm',
    console=True,
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
    name='create-master-vm'
)
