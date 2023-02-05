from collections import defaultdict
import json
import os
import requests
import scrapy

def format_news_for_line_notification(date, news_json):
    result = []
    for item in news_json:
        result.append('') 
        result.append(date)
        result.append(item['category'])
        result.append(item['title'])
        result.append(item['link'])
        result.append('') 

    formatted_news = '\n'.join(result)
    return formatted_news

def send_line_notification(notification_contents):
    # LINE_NOTIFY_TOKEN= os.environ["LINE_NOTIFY_TOKEN"]
    # api_url = "https://notify-api.line.me/api/notify"

    # send_contents = notification_contents

    # TOKEN_dic = {"Authorization": "Bearer" + " " + LINE_NOTIFY_TOKEN}
    # send_dic = {"message": send_contents}
    # requests.post(api_url, headers=TOKEN_dic, data=send_dic)
    print (notification_contents)

class KanteiSpider(scrapy.Spider):
    name = 'kantei'
    allowed_domains = ['kantei.go.jp']
    start_urls = ['https://www.kantei.go.jp/jp/joho/news/index.html']
    
    def parse(self, response):
        li_list= []
        
        # 官邸の1ページ目のliのリスト取得
        res = response.css('div.section>ul>li')
        for li in res:
            item = {
              'date': li.css('div.news-list-date::text').get(),
              'category': li.css('div.news-label::text').get(),
              'title': li.css('div.news-list-title>a::text').get(),
              'link': li.css('div.news-list-title>a::attr(href)').get(),
            }
            li_list.append(item)

        # 日付ごとにリスト化
        news_by_date = defaultdict(list)
        for d in li_list:
            date = d['date']
            news_by_date[date].append(
              {'category': d['category'], 'title': d['title'], 'link': d['link']})

        # 日付ごとにファイル更新
        data_dir = 'crawler/data/'
        for date, date_news in news_by_date.items():
            if not os.path.exists(f'{data_dir}{date}.json'):
                # ファイルがなければ作成
                with open(f'{data_dir}{date}.json', 'w', encoding='utf-8') as f:
                    json.dump(date_news, f, indent=4, ensure_ascii=False)
                with open(f'crawler/data/create.json', 'w', encoding='utf-8') as f:
                    json.dump(f'{data_dir}{date}', f, indent=4, ensure_ascii=False)

                print(f'{data_dir}{date}に新規出力')

                # send_line_notification(format_news_for_line_notification(date, date_news))
            else:
                # ファイルがあり、かつ差分があれば追記
                with open(f'{data_dir}{date}.json') as f:
                    previous_data = json.load(f)
                    diff_data = [d for d in date_news if d not in previous_data]
                    if len(diff_data) > 0:
                        previous_data.extend(diff_data)
                        with open(f'{data_dir}{date}.json', 'w', encoding='utf-8') as f:
                            json.dump(previous_data, f, indent=4, ensure_ascii=False)
                        with open('crawler/data/update.json', 'w', encoding='utf-8') as f:
                            json.dump(f'{data_dir}{date}', f, indent=4, ensure_ascii=False)
                        
                        print(f'{data_dir}{date}に差分出力')
                        
                        # LINE Notifyで差分を通知
                        # send_line_notification(format_news_for_line_notification(date, diff_data))