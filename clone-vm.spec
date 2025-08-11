# clone-vm.spec
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import VSVersionInfo

block_cipher = None

# Version information that will be compiled into the executable.
# Note: This is static and not updated by the versioning script.
# The official version is tracked by the Git tag.
vinfo = VSVersionInfo(
    filevers=(1, 4, 3, 0),
    prodvers=(1, 4, 3, 0),
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
    # Use the version info object for cross-platform compatibility.
    version=vinfo
)
