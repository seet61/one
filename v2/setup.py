#setup.py
from cx_Freeze import setup, Executable as cxExecutable
import platform, sys
 
base = None
if sys.platform == "win32":
    base = "Console"
 
build_exe_options = {
    "base": base,
    "compressed" : True,
    "create_shared_zip" : True,
    "packages": ["os", "sys", "shutil", "vk", "logging", "requests", "urllib.request", "connect", "manipulation"],
    #"icon" : ["Mafia-2-3-icon"],
    "include_files" : [
        "readme.txt"
    ]
}
 
WIN_Target = cxExecutable(script = "audio_sync.py",
    targetName = "vksync.exe",
    compress = True,
    appendScriptToLibrary = False,
    appendScriptToExe = True)
 
setup(  name = "vkMusicSync",
        version = "0.2",
        description = "vkMusicSync",
        options = {"build_exe": build_exe_options},
        executables = [WIN_Target])
