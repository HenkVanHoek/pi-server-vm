# clone-vm.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

import sys
binaries_list = []

if sys.platform == 'win32':
    from PyInstaller.utils.hooks import collect_dynamic_libs
    binaries_list = collect_dynamic_libs('python')

a = Analysis(
    ['clone_vm.py'],
    binaries=binaries_list
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='clone-vm',
    console=True,
    upx=True,
    # Point directly to the version info file.
    version='file_version_info.txt'
)
