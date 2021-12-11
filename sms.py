from zeep import Client
url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
client = Client(url)
userName = 'USERNAME'
password = 'PASSWORD'
recipientNumber = '017…'
smsText = 'Hello Python'
smsType = 'TEXT'
maskName = ''
campaignName = ''
client.service.OneToOne(userName,password,recipientNumber,smsText,smsType,maskName,campaignName)