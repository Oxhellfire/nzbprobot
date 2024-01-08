from re import findall
from nzbpro import nzbprolog
from nzbpro.helpers.sabnzbd_apis import SabnzbdAPIs
from nzbpro.helpers.extra_utils import set_interval, DownloadStatus, get_status_msg


sabnzbd = SabnzbdAPIs()

class SabnzbdDownloader:
    def __init__(self):
        pass
    
    
    async def onDlStart(self):
        await set_interval(2, self.onDlProgress)
    
    
    async def onDlProgress(self):
        queue = await sabnzbd.queue()
        queue_slots = queue['queue']
        history = await sabnzbd.history()
        history_slots = history['history']['slots']
        
        progress = ""
        
        if queue_slots:
            _speed = queue_slots['speed'] + "B"
            for q_slot in queue_slots['slots']:
                mb = float(q_slot['mb'])
                mbleft = float(q_slot['mbleft'])
                status = (
                    DownloadStatus.STATUS_WAITING 
                    if q_slot['status'] == DownloadStatus.STATUS_DOWNLOADING and mbleft == mb 
                    else q_slot['status']
                )
                task_id = q_slot['nzo_id']
                name = q_slot['filename']
                size = q_slot['size'] if status == DownloadStatus.STATUS_DOWNLOADING else '0'
                percentage = float(q_slot['percentage'])
                eta = q_slot['timeleft'] if status == DownloadStatus.STATUS_DOWNLOADING else '0:00:00'
                
                if status == DownloadStatus.STATUS_GRABBING:
                    status = DownloadStatus.STATUS_FETCHING
                    name = "Getting Details From NZB"
                inc_size = 0
                
                if status == DownloadStatus.STATUS_DOWNLOADING:
                    _size = 0
                    dec = mb - mbleft
                    _size += max(0, dec)
                    inc_size = min(mb, _size)
            
                transferred = f"{round(inc_size, 1)} MB"
                speed = _speed if status == DownloadStatus.STATUS_DOWNLOADING else 0
                progress += get_status_msg(status, name, percentage, transferred, size, speed, eta, task_id)
        
        if history_slots:
            h_slot = history_slots[-1]
            action_line = h_slot['action_line']
            if data := findall(r'.+:.{3}([\d.]+.).{4}([\d.]+.{3}).{8}(\d+).{4}([\d.]+.{3}).{10}(\d+\w+)', action_line):
                transferred, size, percentage, speed, eta = data[0]
                transferred += "B"
            name = h_slot['name']
            task_id = h_slot['nzo_id']
            status = h_slot['status']
            if status == DownloadStatus.STATUS_RUNNING:
                status = DownloadStatus.STATUS_UPLOADING
                
            if status == DownloadStatus.STATUS_COMPLETED:
                await self.clear_history(task_id)
        
            progress += get_status_msg(status, name, percentage, transferred, size, speed, eta, task_id)
        
        
        return progress

    
    async def add_sabnzbd_download(self, nzb_file_path=None, nzb_ids=None):
        if nzb_file_path is not None:
            await sabnzbd.add_file(nzb_file_path)
        elif nzb_ids is not None:
            for nzb_id in nzb_ids:
                await sabnzbd.add_url(nzb_id)

        await self.onDlStart()
        nzbprolog.info(f"Task[s] Added {nzb_ids if nzb_file_path is None else nzb_file_path}")
                
    
    async def clear_queue(self, task_id):
        status = await sabnzbd.delete_queue(task_id)
        try:
            if status['status']:
                nzbprolog.info(f"Task Queue Cancel {task_id}")
        except:
            pass
        
        
    async def clear_history(self, task_id):
        status = await sabnzbd.delete_history(task_id)
        try:
            if status['status']:
                nzbprolog.info(f"Task History Cancel {task_id}")
        except:
            pass
        
        
    async def cancel_history_upload(self, task_id):
        status = await sabnzbd.cancel_upload(task_id)
        try:
            if status['status']:
                nzbprolog.info(f"Task History Upload Cancel {task_id}")
        except:
            pass
        
        
    async def clear_all(self):
        await sabnzbd.delete_queue_all()
        await sabnzbd.delete_history_all()
        nzbprolog.info("Cleared All Queues/Histories")