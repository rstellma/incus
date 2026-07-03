Type | Version/Name
--- | ---
Distribution Name	| OpenSuSE Leap
Distribution Version	| 16.0
Kernel Version	| 6.12.0-160000.35-default
Architecture	| x86\_64
Incus Version	| 6.23
Xephyr Version | 21.1.15
Created | 2026-07-01
Updated | 2026-07-03

Container | Profile | Start (incus exec \<container\> -- sudo -u ralf -E)
--- | --- | ---
chromium | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_Chromium</li></ul> | chromium
firefox | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_Firefox</li></ul> | firefox
libreoffice | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_LibreOffice</li></ul> | <ul><li>libreoffice --base</li><li>libreoffice --calc</li><li>libreoffice --draw</li><li>libreoffice --impress</li><li>libreoffice --math</li><li>libreoffice --writer</li></ul>
mutt1 | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_mutt1</li></ul> | bash -c 'cd $HOME; mutt'
mutt2 | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_mutt2</li></ul> | bash -c 'cd $HOME; mutt'
newsboat | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>11-Users</li><li>20-Apps_w3m</li></ul> | bash -c 'cd $HOME; newsboat'
opera | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>10-GUI</li><li>11-Users</li><li>20-Apps_Opera</li></ul> | opera
w3m | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>11-Users</li><li>20-Apps_w3m</li></ul> | bash -c 'cd $HOME; w3m -B ./.w3m/bookmark.html<br/> -config ./.w3m/config'
yt-dlp | <ul><li>00-Container_Storage</li><li>01-Container_Network</li><li>01-Container_ResLimits</li><li>11-Users</li><li>20-Apps_ytdlp</li></ul> | bash -c 'cd $HOME'

- **Fluxbox** in Container "desktop" starten (default)
```bash
$> ./start-desktop.sh [fluxbox]
```

- **KDE** in Container "desktop" starten
```bash
$> ./start-desktop.sh kde
```

- **Fluxbox** oder **KDE** in Container "foo" starten
```bash
$> ./start-desktop.sh fluxbox|kde foo
```
