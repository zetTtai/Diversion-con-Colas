C:
Set-Location /
New-Item kafka -ItemType Directory
Set-Location kafka
Invoke-WebRequest https://archive.apache.org/dist/kafka/2.8.1/kafka_2.13-2.8.1.tgz -OutFile kafka.tgz
tar -xzf kafka.tgz
Get-ChildItem -Path kafka_2.13-2.8.1 -Recurse -File | Move-Item -Destination .
Remove-Item kafka.tgz
Remove-Item kafka_2.13-2.8.1