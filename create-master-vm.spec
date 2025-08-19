# create-master-vm.spec (Directory Build Test)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs

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
    exclude_binaries=True, # Exclude from EXE, will be in COLLECT
    name='create-master-vm',
    console=True,
    upx=True,
    version='file_version_info.txt'
)

# The COLLECT object creates the final output directory
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='create-master-vm'
)
