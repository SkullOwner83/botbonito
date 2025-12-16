import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

project_path = os.getcwd()

# Recorrer carpeta assets para incluir todos los archivos y subcarpetas
datas = []
assets_path = os.path.join(project_path, 'assets')
for root, dirs, files in os.walk(assets_path):
    for f in files:
        full_path = os.path.join(root, f)
        # Guardar con ruta relativa (ej: assets/... )
        rel_path = os.path.relpath(full_path, project_path)
        datas.append((full_path, os.path.dirname(rel_path)))

a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BotBonito',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BotBonito'
)