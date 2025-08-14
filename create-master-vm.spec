# create-master-vm.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

import sys
binaries_list = []

if sys.platform == 'win32':
    from PyInstaller.utils.hooks import collect_dynamic_libs
    binaries_list = collect_dynamic_libs('python')

a = Analysis(
    ['run_create_master.py'],
    # This 'binaries' argument is the fix.
    # It tells PyInstaller to find and bundle all the DLLs
    # that the Python interpreter itself depends on.
    binaries=binaries_list
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='create-master-vm',
    console=True,
    upx=True,
    # Point directly to the version info file.
    version='file_version_info.txt'
)
