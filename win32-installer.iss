; Inno install packager

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{02032A04-CEBD-4E65-9433-A700D205AC32}
AppName=Zoxel
#define VERSION "0.5.0pre3"
AppVersion={#VERSION}
AppPublisher=Graham R King
AppPublisherURL=http://zoxel.blogspot.co.uk
AppSupportURL=http://zoxel.blogspot.co.uk
AppUpdatesURL=http://zoxel.blogspot.co.uk
DefaultDirName={pf}\Zoxel
DefaultGroupName=Zoxel
OutputDir=C:\Source\zoxel\install
OutputBaseFilename=zoxel-{#VERSION}-win32
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\zoxel.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Zoxel"; Filename: "{app}\zoxel.exe"
Name: "{group}\{cm:UninstallProgram,Zoxel}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Zoxel"; Filename: "{app}\zoxel.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\zoxel.exe"; Description: "{cm:LaunchProgram,Zoxel}"; Flags: nowait postinstall skipifsilent

