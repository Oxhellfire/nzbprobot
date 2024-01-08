import requests
from nzbpro import S_ENDPOINT, NZB_URL
from nzbpro.helpers.extra_utils import fetch_data


class SabnzbdAPIs():
    def __init__(self):
        pass
        
        
    async def add_url(self, nzo_id):
        url = f"{NZB_URL}/{nzo_id}"
        if requests.get(url).status_code != 200:
            return "Not a Valid ID Please Provide a Valid ID!"
        params = {"mode": "addurl", "name": url}
        res = await fetch_data(S_ENDPOINT, params)
        return res
        
        
    async def add_file(self, path):
        params = {"mode": "addlocalfile", "name": path}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def queue(self):
        params = {"mode": "queue"}
        res = await fetch_data(S_ENDPOINT, params, "dict")
        return res
    
    
    async def history(self):
        params = {"mode": "history"}
        res = await fetch_data(S_ENDPOINT, params, "dict")
        return res
    
    
    async def pause_single(self, nzo_id):
        params = {"mode": "queue", "name": "pause", "value": nzo_id}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def resume_single(self, nzo_id):
        params = {"mode": "queue", "name": "resume", "value": nzo_id}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def delete_queue(self, nzo_id):
        params = {"mode": "queue", "name": "delete", "value": nzo_id}
        res = await fetch_data(S_ENDPOINT, params, "dict")
        return res
    
    
    async def pasue_all(self):
        params = {"mode": "pause"}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def resume_all(self):
        params = {"mode": "resume"}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def delete_queue_all(self):
        params = {"mode": "queue", "name": "delete", "value": "all", "del_files": 1}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def purge_via_keyword(self, keyword):
        params = {"mode": "queue", "name": "purge", "search": keyword, "del_files": 1}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def delete_history(self, nzo_id):
        params = {"mode": "history", "name": "delete", "value": nzo_id}
        res = await fetch_data(S_ENDPOINT, params, "dict")
        return res
    
    
    async def delete_history_all(self):
        params = {"mode": "history", "name": "delete", "value": "all"}
        res = await fetch_data(S_ENDPOINT, params)
        return res
    
    
    async def cancel_upload(self, task_id):
        params = {"mode": "cancel_pp", "value": task_id}
        res = await fetch_data(S_ENDPOINT, params, "dict")
        return res