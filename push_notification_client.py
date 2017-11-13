import requests
import json

class FCMPushClient(object):
	"""docstring for PushClient"""
	def __init__(self, api_key,url):
		self.api_key=api_key
		self.content="application/json"
		self.url=url
		self.header={
			"Content-type":self.content,
	 		"Authorization": "key=" + self.api_key
		}



	def send_topic(self,topic, notification, data={}):
		"""
		Des:
		params: topic: str  
				notification: dict  structure {"title":"", "body":"", "icon":""}
				data: dict 

		"""
		if data=={}:
			request={"to":"/topics/"+topic, "notification":notification}
		else:
			request={"to":"/topics/"+topic, "notification":notification, "data":data}

		response=requests.post(url=self.url, headers=self.header, data=json.dumps(request))

		json_response=json.loads(response.text)

		print(json_response)

		if "message_id" in json_response:
			return {"code":"00", "msg":"Successfully Sent Notifications"}

		return json_response


	def send_multiple(self,reg_ids, notification, data={}):

		"""
		Des:
		params: reg_ids:list contains list of a registration ids   
				notification: dict  structure {"title":"", "body":"", "icon":""}
				data: dict 

		"""
		if data=={}:
			request={"to":json.dumps(reg_ids), "notification":notification}
		else:
			request={"to":json.dumps(reg_ids), "notification":notification, "data":data}

		response=requests.post(url=self.url, headers=self.header, data=json.dumps(request))

		json_response=json.loads(response.text)


		if "message_id" in json_response:
			return {"code":"00", "msg":"Successfully Sent Notifications"}

		return json_response


	def send_single(self,reg_id, notification, data={}):
		"""
		Des:
		params: reg_id: str  
				notification: dict  structure {"title":"", "body":"", "icon":""}
				data: dict 

		"""
		if data=={}:
			request={"to":reg_id, "notification":notification}
		else:
			request={"to":reg_id, "notification":notification, "data":data}

		response=requests.post(url=self.url, headers=self.header, data=json.dumps(request))

		json_response=json.loads(response.text)

		if "message_id" in json_response:
			return {"code":"00", "msg":"Successfully Sent Notifications"}

		return json_response




		