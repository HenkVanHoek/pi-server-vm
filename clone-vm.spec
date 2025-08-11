# clone-vm.spec
# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

# Initialize vinfo to None for non-Windows platforms.
vinfo = None

# Only create the version info object if we are building on Windows.
if sys.platform.startswith('win32'):
    from PyInstaller.utils.win32.versioninfo import (
        VSVersionInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct
    )
    vinfo = VSVersionInfo(
        file_version=(1, 4, 3, 0),
        product_version=(1, 4, 3, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
        kids=[
            StringFileInfo(
                [
                    StringTable(
                        u'040904B0',
                        [
                            StringStruct(u'CompanyName', u'PiSelfhosting'),
                            StringStruct(u'FileDescription', u'Clones a VirtualBox master template for automated testing.'),
                            StringStruct(u'FileVersion', u'1.4.3.0'),
                            StringStruct(u'InternalName', u'clone-vm'),
                            StringStruct(u'LegalCopyright', u'© 2025 Henk van Hoek. All rights reserved.'),
                            StringStruct(u'OriginalFilename', u'clone-vm.exe'),
                            StringStruct(u'ProductName', u'PiSelfhosting'),
                        ]
                    )
                ]
            ),
            VarFileInfo([VarStruct(u'Translation',)])
        ]
    )

a = Analysis(
    ['run_clone.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    a.binaries,
    a.datas,
    name='clone-vm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    version=vinfo
)
