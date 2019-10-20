import json
import requests

from utils import timestamp, weekday

KEYS = ['天气', '时间']

class GCAI(object):

    def req(self, url):
        res = None
        resp = requests.get(url)
        if 200 == resp.status_code:
            res = resp.text
        return res

    def get_weather(self):
        res = '不知道'
        data = json.loads(self.req('https://free-api.heweather.net/s6/weather/now?location=beijing&key=44061e474705463f82abf7620972991e'))
        if data is not None:
            j = data.get('HeWeather6')[0]
            loc = j.get('basic').get('location')
            now = j.get('now')
            wea = now.get('cond_txt')
            temp = now.get('tmp')
            res = '地点' + loc + '天气' + wea + '温度' + temp
        return res

    def get_datetime(self):
        return timestamp(fmt='%Y年%m月%d日%H时%M分%S秒') + '星期' + weekday()

    def _baidu(self, msg):
        data = self.req('https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=' + msg + '&cb=showData')[len('showData('): -2]
        l = eval(data[data.find('s:[') + len('s:[')-1: -1])
        return ' '.join(l)

    def _bing(self, msg):
        from azure.cognitiveservices.search.websearch import WebSearchAPI
        from azure.cognitiveservices.search.websearch.models import SafeSearch
        from msrest.authentication import CognitiveServicesCredentials
        subscription_key = "YOUR_SUBSCRIPTION_KEY"
        client = WebSearchAPI(CognitiveServicesCredentials(subscription_key), base_url = "YOUR_ENDPOINT")
        web_data = client.web.search(query=msg)
        if hasattr(web_data.web_pages, 'value'):
            first_web_page = web_data.web_pages.value[0]
            print("First web page name: {} ".format(first_web_page.name))
            print("First web page URL: {} ".format(first_web_page.url))
        else:
            print("Didn't find any web pages...")
        if hasattr(web_data.images, 'value'):

            print("\r\nImage Results#{}".format(len(web_data.images.value)))

            first_image = web_data.images.value[0]
            print("First Image name: {} ".format(first_image.name))
            print("First Image URL: {} ".format(first_image.url))

        else:
            print("Didn't find any images...")

        '''
        News
        If the search response contains news, the first result's name and url
        are printed.
        '''
        if hasattr(web_data.news, 'value'):

            print("\r\nNews Results#{}".format(len(web_data.news.value)))

            first_news = web_data.news.value[0]
            print("First News name: {} ".format(first_news.name))
            print("First News URL: {} ".format(first_news.url))

        else:
            print("Didn't find any news...")

        '''
        If the search response contains videos, the first result's name and url
        are printed.
        '''
        if hasattr(web_data.videos, 'value'):

            print("\r\nVideos Results#{}".format(len(web_data.videos.value)))

            first_video = web_data.videos.value[0]
            print("First Videos name: {} ".format(first_video.name))
            print("First Videos URL: {} ".format(first_video.url))

        else:
            print("Didn't find any videos...")

    def search(self, msg, engine='baidu'):
        if 'baidu' == engine:
            res = self._baidu(msg)
        elif 'bing' == engine:
            res = self._bing(msg)
        res = res.strip()
        if 1000 < len(res):
            res = res[:1000]
        return res


if __name__ == "__main__":
    g = GCAI()
    print(g.search('北京', 'baidu'))