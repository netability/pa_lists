# Update Lists for PA
Palo Alto External dynamic Lists
-------------
Microsoft 365

https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7

Save the file worldwide.json and run the python microsoft_lists.py, you will have 2 files ip and url

*************
AWS

(*) Install-Module -Name AWS.Tools.Installer

(*) Install-AWSToolsModule AWS.Tools.EC2,AWS.Tools.S3 -CleanUp

(Get-AWSPublicIpAddressRange).IpPrefix > exportaws.txt

(*) first time only

*************
Duo

https://help.duo.com/s/article/1337?language=en_US

*************
Proofpoint

https://help.proofpoint.com/Proofpoint_Essentials/Email_Security/Administrator_Topics/000_gettingstarted/020_connectiondetails

*************
CloudFlare

https://www.cloudflare.com/ips/

*************
Manual Block IPs or URLs - Follow MAS or urgent

IP_block.txt

URL_Block.txt

*************
Google

https://www.gstatic.com/ipranges/goog.json

https://www.gstatic.com/ipranges/cloud.json

Save the first google1.json and the second google2.json
Run the python google_lists.py


*************
Checkpoint IPs and URL

https://support.checkpoint.com/results/sk/sk116590
