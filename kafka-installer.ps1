$Kafka_Command_Path = ".\bin\windows\zookeper-server-start.bat"
$Kafka_Config_File = ".\config\zookeeper.properties"

C:
Set-Location /
New-Item kafka -ItemType Directory
Set-Location kafka
Invoke-WebRequest https://github.com/zetTtai/Diversion-con-Colas/blob/Kafka-Installer/Kafka.zip?raw=true -OutFile kafka.zip
Expand-Archive -Path kafka.zip -DestinationPath .
Get-ChildItem -Path Kafka -Recurse -File | Move-Item -Destination .
#Remove-Item kafka.tgz
Remove-Item Kafka
cmd.exe         .\bin\windows\zookeper-server-start.bat                 .\config\zookeeper.properties
Invoke-Command  .\bin\windows\kafka-server-start.bat     -ArgumentList  .\config\server.properties