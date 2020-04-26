Set ServiceName=mongodb
SC queryex "%ServiceName%"|Find "STATE"|Find /v "RUNNING">Nul&&(
echo %ServiceName% not running
Net start "%ServiceName%"
)||(
echo "%ServiceName%" is working
)
timeout 5