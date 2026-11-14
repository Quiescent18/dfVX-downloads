"""Verify and package dfVX 1.0 Windows VST3 from a successful private CI artifact."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib

src=Path("dfvx-vst3-build.zip")
manual=Path("dfVX_User_Manual_1.0.pdf")
output=Path("dfVX-1.0.0-Windows-VST3-x64.zip")
notes=Path("RELEASE_NOTES.txt")
readme="""dfVX 1.0 - Windows x64 VST3
Kisatchie Audio

INSTALLATION
1. Extract this ZIP completely.
2. Close your DAW.
3. Copy the entire dfVX.vst3 folder into:
   C:\\Program Files\\Common Files\\VST3
4. Restart your DAW and rescan VST3 plugins if needed.

The full illustrated user manual is included with this download.
This is a VST3 plugin, not a standalone application.
No development libraries or source files are distributed.
For updates, replace the whole VST3 folder while your DAW is closed.
User presets live in Documents\\dfVX\\Presets.
The software is not digitally signed.
"""
if not manual.exists() or manual.stat().st_size<1000000:
    raise RuntimeError("Updated illustrated manual was not successfully generated")
with ZipFile(src) as build:
    assert build.testzip() is None, "Build ZIP is corrupt"
    entries=[n for n in build.namelist() if n.startswith("dfVX.vst3/") and not n.endswith("/")]
    assert "dfVX.vst3/Contents/x86_64-win/dfVX.vst3" in entries
    assert len(entries)>=2
    module=build.read("dfVX.vst3/Contents/Resources/moduleinfo.json").decode()
    assert '"Version": "1.0.0"' in module, "Wrong plugin version"
    assert '"Name": "dfVX"' in module and '"Vendor": "Kisatchie Audio"' in module
    assert not any(n.lower().endswith((".exp",".lib")) for n in entries)
    with ZipFile(output,"w",ZIP_DEFLATED,compresslevel=9) as pack:
        for name in entries: pack.writestr(name,build.read(name))
        pack.writestr("README.txt",readme)
        pack.write(notes,"RELEASE_NOTES.txt")
        pack.write(manual,"dfVX_User_Manual_1.0.pdf")
with ZipFile(output) as check:
    assert check.testzip() is None
    assert len(check.namelist())==len(entries)+3
    assert not any(n.lower().endswith((".exp",".lib")) for n in check.namelist())
    assert check.read("dfVX_User_Manual_1.0.pdf")==manual.read_bytes()
hashfn=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
Path("SHA256SUMS.txt").write_text(
    f"{hashfn(output)}  {output.name}\n{hashfn(manual)}  {manual.name}\n")
print("Packaged verified dfVX 1.0 VST3",output.stat().st_size,"bytes")
