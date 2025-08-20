; installer.iss
; Inno Setup script for the Pi-Server-VM Tools project.

[Setup]
; --- Basic Application Information ---
AppName=Pi-Server-VM Tools
; The version is passed in from our release.py script
AppVersion={#MyVersion}
AppPublisher=PiSelfhosting
DefaultDirName={autopf}\Pi-Server-VM Tools
DefaultGroupName=Pi-Server-VM Tools

; --- Installer Output ---
; The final setup-x.x.x.exe will be placed in the 'dist' directory
OutputBaseFilename=pi-server-vm-setup-{#MyVersion}
OutputDir=./dist
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
; This is the most important section.
; It tells the installer to take all the directories and files from our
; PyInstaller build output ('dist' folder) and package them.
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; This section creates the Start Menu shortcuts for the user.
Name: "{group}\Create Master VM"; Filename: "{app}\create-master-vm\create-master-vm.exe"
Name: "{group}\Clone VM"; Filename: "{app}\clone-vm\clone-vm.exe"
Name: "{group}\Web App"; Filename: "{app}\pi-selfhosting-web\pi-selfhosting-web.exe"
Name: "{group}\Uninstall Pi-Server-VM Tools"; Filename: "{uninstallexe}"
