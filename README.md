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

https://help.proofpoint.com/Proofpoint_Essentials/Email_Security/Administrator_Topics/000_gettingstarted/020_connectiondetails (not in use)
https://help.proofpoint.com/Essentials/Product_Documentation/Email_Security/Mail_Services/01_Connection_Details
Copy source: Right-click on the page > View Page Source (or Ctrl+U). Select all (Ctrl+A) > Copy (Ctrl+C).
Save file: Open Notepad > Paste (Ctrl+V) > Save As > Name it exactly proofpoint_page.html > In the same folder as this Python script.

Run python proofpoint.py

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

Save the first goog.json and the second cloud.json
Run the python google_lists.py


*************
Checkpoint IPs and URL

https://support.checkpoint.com/results/sk/sk116590

*************
Apple IPs and URL

Run python apple.py he will generate 2 files
