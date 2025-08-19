# clone-vm.spec (Final, Definitive Version)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs
import sys

block_cipher = None

if sys.platform == "win32":
    dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
    python_dir = os.path.dirname(sys.executable)
    python_dll = os.path.join(python_dir, dll_name)
    binaries = collect_dynamic_libs('python')
    if os.path.exists(python_dll):
        print(f"PYI-DEBUG: Adding {python_dll} to _internal")
        binaries.append((python_dll, '_internal'))
    else:
        print(f"PYI-DEBUG: python_dll not found at {python_dll}")
else:
    binaries = collect_dynamic_libs('python')

a = Analysis(
    ['run_clone.py'],
    binaries=binaries,
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
    version='file_version_info.txt',
    onefile=True
)
