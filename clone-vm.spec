# clone-vm.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(['run_clone.py'])
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
