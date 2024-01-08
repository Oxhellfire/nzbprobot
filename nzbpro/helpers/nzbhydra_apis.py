from lxml import etree
from datetime import datetime
from urllib.parse import urlparse
from nzbpro import H_ENDPOINT, H_INDEXERS
from nzbpro.helpers.extra_utils import fetch_data, telegraph_page, get_size


# Indexers Websites
INDEXERS_WEBSITES = {
    "abNZB": "https://abnzb.com/register",
    "NZB Finder": "https://nzbfinder.ws/register",
    "nzb.su": "https://api.nzb.su/register",
    "NZBGeek": "https://nzbgeek.info/register.php",
    "NzBNooB": "https://www.nzbnoob.com/register",
    "nzbplanet": "https://nzbplanet.net/registerpremium",
    "altHUB": "https://althub.co.za/register",
    "Animetosho (Newznab)": "https://animetosho.org/register",
    "miatrix": "https://www.miatrix.com/register",
}


class HydraHelper:
    def __init__(self):
        pass
                
                
    async def parse_xml_data(self, query, res):
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(res.encode('utf-8'), parser=parser)

        namespaces = {'newznab': 'http://www.newznab.com/DTD/2010/feeds/attributes/'}
        indexer = root.xpath('//newznab:attr[@name="hydraIndexerName"]', namespaces=namespaces)
        item = root.xpath("//item")
        
        if not item:
            return "No Result Found!"
        
        result_msg = "".join(
            f"<b>{item.find('title').text}</b><br>"
            f"[ {get_size(int(item.find('size').text))} | "
            f"<a href='{urlparse(item.find('comments').text).scheme}://{urlparse(item.find('comments').text).netloc}/'>{indexer.get('value')}</a> | "
            f"{item.find('category').text} | "
            f"{self.get_days(item.find('pubDate').text)} days ]<br>"
            f"<pre>{item.find('guid').text}</pre><br>"
            for index, (indexer, item) in enumerate(zip(indexer, item)) if index <= 75
        )

        res = telegraph_page(query, result_msg)
        return res
    
    
    def get_days(self, pubDate):
        nzb = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z")
        current = datetime.now(nzb.tzinfo)
        days = (current - nzb).days
        return days

                
    async def query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "search", "q": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def series_query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "tvsearch", "q": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def movie_query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "movie", "q": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def book_query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "book", "q": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def imdb_series_query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "tvsearch", "imdbid": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def imdb_movie_query(self, query):
        res = await fetch_data(
            H_ENDPOINT, params={"t": "movie", "imdbid": query}
        )
        return await self.parse_xml_data(query, res)
    
    
    async def indexers(self):
        res = await fetch_data(H_INDEXERS, None, "dict")
        return [
            f"{indexer['indexerName']}" for indexer in res["indexerApiAccessStats"]
        ]
