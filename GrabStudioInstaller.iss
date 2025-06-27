; -- GrabStudioInstaller.iss --
; Script d'installation pour YouTube Grab Studio

[Setup]
AppName=Grab Studio Pro
AppVersion=2.3.23
AppPublisher=EnokSeth
DefaultDirName={autopf}\YouTube Grab Studio
DefaultGroupName=YouTube Grab Studio
OutputDir=userdocs:Inno Setup Builds
OutputBaseFilename=GrabStudioSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\GrabStudio.exe

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; DestName: "GrabStudio.exe"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"
; Facultatif : Readme ou autres fichiers
; Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Grab Studio Pro"; Filename: "{app}\GrabStudio.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\Grab Studio Pro"; Filename: "{app}\GrabStudio.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le bureau"; GroupDescription: "Icônes supplémentaires:"

[Run]
Filename: "{app}\GrabStudio.exe"; Description: "Lancer Grab Studio"; Flags: nowait postinstall skipifsilent
