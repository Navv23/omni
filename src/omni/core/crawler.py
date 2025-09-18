import requests
from bs4 import BeautifulSoup
from omni.settings import load_source_sites
from urllib.parse import urlencode


class GoogleNewsCrawler:
    def __init__(self):
        self.base_url = "https://news.google.com"

    def _get_source_sites(self, financial_flag: bool=False):
        '''
        Get a list of general or financial websites.
        '''
        sites = load_source_sites()
        if financial_flag:
            financial_websites = sites.get('financial_websites', '')
            return financial_websites
        else:
            general_websites = sites.get('general_websites', '')
            return general_websites
        
    def _construct_url_with_filters(self, search=None, time_period=None, financial_flag: bool=False):
        '''
        Constructs a Google News search URL with optional filters.
        '''
        all_urls = []
        params = {}

        sites = self._get_source_sites(financial_flag=financial_flag)

        for site in sites:
            params["q"] = f"{search} source:{site} when:{time_period}"
            query_string = urlencode(params)
            all_urls.append(f"{self.base_url}/search?{query_string}")
        return all_urls

    def _fetch_page(self, url: str):
        '''
        Fetches the page and returns context.
        '''
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        return {"status_code": response.status_code, "content": response.text}

    def _crawl_page(self, context):
        '''
        Parses context from the fetched HTML content.
        '''
        soup = BeautifulSoup(context["content"], "html.parser")
        data_store = []
        for article in soup.find_all("c-wiz", class_="XBspb"):
            title = article.find('a', class_='''JtKRv''').text
            time_posted = article.find('time', class_='''hvbAAd''').text
            source = article.find('div', class_='''vr1PYe''').text
            
            data_store.append({"title": title,
                               "time_posted": time_posted,
                               "source": source})

        return data_store


    def run(self, search: str = None, time_period: str = '7d', financial_flag: bool = False):
        '''
        Main method
        '''
        content = []
        source_urls = self._construct_url_with_filters(search=search,
                                                          time_period=time_period,
                                                          financial_flag=financial_flag)
        
        for url in source_urls:
            context = self._fetch_page(url=url)
            results = self._crawl_page(context=context)
            for result in results:
                content.append((result.get('title', ''), result.get('time_posted', '')))
        
        return content


if __name__ == "__main__":
    crawler = GoogleNewsCrawler()
    crawler.run(search='Technology News', time_period='1d', financial_flag=False)