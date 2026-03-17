import requests
import felog.core as felog
from typing import Optional, List, Any


class Phone:
    def __init__(self,key: Optional[str] = None, baseurl: Optional[str] = None) -> None:
        self.log = felog.log("Quo",debug=False)
        self.__connected: bool = False
        self.__phone_id: str = None
        self.__phone_number: str = None
        self.__key: str = key
        self.__baseurl: str
        if baseurl:
            self.__baseurl = baseurl
        else:
            self.__baseurl = "https://api.openphone.com"

    def convert_to_e164(self, number: str, countrycode: Optional[str] = "1") -> str:
        parsed_num = number.replace("(","").replace(")","").replace("-","").replace(".","").replace(" ","").strip()
        num = f"+{countrycode}{parsed_num}"
        return num

    def party_lst_to_str(self, participants: List[Any]) -> str:
        partystr: str = ','.join(participants)
        return partystr
    
    def party_str_to_list(self, participants: str) -> List[Any]:
        parties: List[str] = participants.split(',')
        return parties
    
    def parse_party_list(self, participants: List[Any]) -> List[Any]:
        parties: List[str] = participants
        for i,p in enumerate(parties):
            tmp = self.convert_to_e164(p)
            parties[i] = tmp
        return parties
    
    def parse_party_str(self, participants: str) -> str:
        parties: List[str] = participants.split(',')
        for i,p in enumerate(parties):
            tmp = self.convert_to_e164(p)
            parties[i] = tmp
        partystr = ','.join(parties)
        return partystr

    def set_api_key(self,key: str) -> bool:
        self.__key = key
        return True
    
    def get_api_key(self) -> str:
        return self.__key
    
    def set_baseurl(self,baseurl: str) -> bool:
        self.__baseurl = baseurl
        return True
    
    def get_baseurl(self) -> str:
        return self.__baseurl
    
    def get_auth(self) -> dict:
        return {'Authorization': self.__key}
    
    def is_connected(self) -> bool:
        return self.__connected
    
    def connect(self) -> bool:
        response = self.get_phone_info()
        if 'number' in response:
            self.__phone_id = response['id']
            self.__phone_number = response['number']
            self.__connected = True
            return True
        return False
    
    def disconnect(self) -> bool:
        if self.__connected:
            self.__phone_id = None
            self.__phone_number = None
            self.__connected = False
            return True
        return False
    
    def show_phone_info(self) -> dict:
        return {'id':self.__phone_id,'number':self.__phone_number}

    def get_phone_info(self) -> dict:
        url = f'{self.__baseurl}/v1/phone-numbers'
        response = requests.get(url, headers=self.get_auth(), timeout=30)
        response_data = response.json()
        if response_data['data'][0]:
            phone_info = {}
            phone_info['id'] = response_data['data'][0]['id']
            phone_info['number'] = response_data['data'][0]['number']
            return phone_info
        else:
            return {'error':'Unable to retrieve phone information.'}
        
    def get_conversations(self, limit: Optional[int] = 100, participants: Optional[str] = None) -> List[Any]:
        paginate: bool = True
        convos: List[Any] = list()
        nextpage: str = None
        payload: dict = {'maxResults': limit}
        # Although Quo's REST API Documentation states that this is technically possible
        # It seems to throw errors every time, so I believe their API may have a bug.
        # We will keep this portion of the code for future updates.
        # if participants:
        #     parties: List[str] = self.party_str_to_list(self.parse_party_str(participants))
        #     payload['phoneNumbers'] = parties
        url = f'{self.__baseurl}/v1/conversations'
        self.log.debug(payload)
        while paginate:
            if nextpage:
                payload['pageToken'] = nextpage
            response = requests.get(url, headers=self.get_auth(), params=payload, timeout=30)
            self.log.debug(response.request.path_url)
            response_data = response.json()
            self.log.debug(response_data)
            data = response_data['data']
            for d in data:
                convos.append(d)
            if response_data.get('nextPageToken'):
                nextpage = response_data['nextPageToken']
            else:
                break
        return convos
    
    def get_messages(self, participants: str, createdbefore: Optional[str] = None, createdafter: Optional[str] = None, limit: Optional[int] = 100) -> List[Any]:
        paginate: bool = True
        messages: List[Any] = list()
        nextpage: str = None
        if not self.is_connected():
            return [{'error':'Phone not connected. You must connect before retrieving calls.'}]
        parties: List[str] = self.party_str_to_list(self.parse_party_str(participants))
        payload: dict = {'maxResults': limit, 'phoneNumberId': self.__phone_id, 'participants': parties}
        self.log.debug(payload)
        url = f'{self.__baseurl}/v1/messages'
        if createdbefore:
            payload['createdBefore'] = createdbefore
        if createdafter:
            payload['createdAfter'] = createdafter
        while paginate:
            if nextpage:
                payload['pageToken'] = nextpage
            response = requests.get(url, headers=self.get_auth(), params=payload, timeout=30)
            response_data = response.json()
            data = response_data['data']
            for d in data:
                messages.append(d)
            if response_data.get('nextPageToken'):
                nextpage = response_data['nextPageToken']
            else:
                break
        return messages
    
    def get_calls(self, participants: str, createdbefore: Optional[str] = None, createdafter: Optional[str] = None, limit: Optional[int] = 100) -> List[Any]:
        paginate: bool = True
        calls: List[Any] = list()
        nextpage: str = None
        if not self.is_connected():
            return [{'error':'Phone not connected. You must connect before retrieving calls.'}]
        parties: List[str] = self.party_str_to_list(self.parse_party_str(participants))
        payload: dict = {'maxResults': limit, 'phoneNumberId': self.__phone_id, 'participants': parties}
        url = f'{self.__baseurl}/v1/calls'
        if createdbefore:
            payload['createdBefore'] = createdbefore
        if createdafter:
            payload['createdAfter'] = createdafter
        while paginate:
            if nextpage:
                payload['pageToken'] = nextpage
            response = requests.get(url, headers=self.get_auth(), params=payload, timeout=30)
            response_data = response.json()
            data = response_data['data']
            for d in data:
                calls.append(d)
            if response_data.get('nextPageToken'):
                nextpage = response_data['nextPageToken']
            else:
                break
        return calls
    
    def send_message(self, participants: str, msgbody: str) -> dict:
        parties: List[str] = self.party_str_to_list(self.parse_party_str(participants))
        if len(msgbody) > 1599:
            return {'error': f'Text message is too long to send. Max is 1,600 characters, you sent: {len(msgbody)}'}
        elif len(msgbody) < 2:
            return {'error': f'Text message is too short to send. Min is 1, you sent: {len(msgbody)}'}
        if not self.is_connected():
            return {'error':'Phone not connected. You must connect before sending text messages.'}
        payload: dict = {'content': msgbody, 'from': self.__phone_id, 'to': parties}
        self.log.debug(payload)
        url = f'{self.__baseurl}/v1/messages'
        response = requests.post(url, headers=self.get_auth(), json=payload, timeout=30)
        response_data = response.json()
        if response_data['data']['status'] == 'sent':
            return response_data['data']
        return {'error': 'Unable to send text message.'}