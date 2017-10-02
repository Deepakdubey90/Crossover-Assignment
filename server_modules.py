class Client:
	ip = None
	alerts = []
	port = None
	username = None
	password = None
	mail = None
	
	def __init__(self,ip):
		self.ip = ip
	
	def append_alert(self,alert):
		self.alerts.append(alert)
		
class Alert:
	alert_type = None
	alert_limit = None
	
	def __init__(self,alert_type,alert_limit):
		self.alert_type = alert_type
		self.alert_limit = alert_limit
	
	
	
