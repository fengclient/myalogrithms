@echo off
echo "configure firewall"
netsh advfirewall firewall add rule name="RDP on 65500 (TCP)" dir=in action=allow enable=yes profile=domain localport=65500 protocol=tcp
echo "enable rdp"
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
echo "modify port as 65500"
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\Tds\tcp" /v PortNumber /t REG_DWORD /d "0x0000ffdc" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v PortNumber /t REG_DWORD /d "0x0000ffdc" /f
echo "restart services"
net stop UmRdpService
net stop TermService
net start TermService
net start UmRdpService
echo "finished."