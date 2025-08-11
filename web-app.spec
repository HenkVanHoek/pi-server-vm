# web-app.spec
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import VSVersionInfo

block_cipher = None

# Version information that will be compiled into the executable.
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
                        StringStruct(u'FileDescription', u'Web interface for PiSelfhosting services.'),
                        StringStruct(u'FileVersion', u'1.4.3.0'),
                        StringStruct(u'InternalName', u'pi-selfhosting-web'),
                        StringStruct(u'LegalCopyright', u'© 2025 Henk van Hoek. All rights reserved.'),
                        StringStruct(u'OriginalFilename', u'pi-selfhosting-web.exe'),
                        StringStruct(u'ProductName', u'PiSelfhosting'),
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct(u'Translation',)])
    ]
)


a = Analysis(
    ['webapp/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('webapp/templates', 'templates'),
        ('webapp/static', 'static')
    ],
    hiddenimports=['waitress'],
    hookspath=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    a.binaries,
    a.datas,
    name='pi-selfhosting-web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    # Use the version info object for cross-platform compatibility.
    version=vinfo
)
