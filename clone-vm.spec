# clone-vm.spec (Final, Definitive Version)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

a = Analysis(
    ['run_clone.py'],
    binaries=collect_dynamic_libs('python'),
    datas=[],
    hiddenimports=[]
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='clone-vm',
    console=True,
    upx=True,
    version='file_version_info.txt'
)
