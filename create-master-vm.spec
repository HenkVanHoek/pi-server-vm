# create-master-vm.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['run_clone.py'],
    # This 'binaries' argument is the fix.
    # It tells PyInstaller to find and bundle all the DLLs
    # that the Python interpreter itself depends on.
    binaries=collect_dynamic_libs('python')
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
