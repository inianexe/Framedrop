[Setup]
AppName=FrameDrop
AppVersion=0.2.0
DefaultDirName={localappdata}\Programs\FrameDrop
DefaultGroupName=FrameDrop
PrivilegesRequired=lowest
OutputDir=release
OutputBaseFilename=FrameDrop-Windows-x64-Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\FrameDrop.exe
[Files]
Source: "dist\FrameDrop\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\FrameDrop"; Filename: "{app}\FrameDrop.exe"
Name: "{autodesktop}\FrameDrop"; Filename: "{app}\FrameDrop.exe"
[Run]
Filename: "{app}\FrameDrop.exe"; Description: "Open FrameDrop"; Flags: nowait postinstall skipifsilent
