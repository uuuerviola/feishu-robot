import feedparser
import requests
import os

# 从 GitHub Secrets 获取配置
RSS_URL = os.environ.get('RSS_URL')
WEBHOOK = os.environ.get('FEISHU_WEBHOOK')

def send_feishu():
    # 1. 抓取 RSS 内容
    feed = feedparser.parse(RSS_URL)
    
    # 如果抓不到，发个报错提醒，不至于静默
    if not feed.entries:
        requests.post(WEBHOOK, json={"msg_type":"text","content":{"text":"❌ 抓取失败：RSS 源没有内容或链接失效"}})
        return

    # 2. 取前 3 条最新资讯
    for entry in feed.entries[:3]:
        title = entry.title
        link = entry.link
        
        # 3. 构造飞书卡片格式
        payload = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "🌍 全球最新资讯速递",
                        "content": [
                            [{"tag": "text", "text": f"标题: {title}"}],
                            [{"tag": "a", "text": "查看原文", "href": link}]
                        ]
                    }
                }
            }
        }
        requests.post(WEBHOOK, json=payload)
        print(f"已发送: {title}")

if __name__ == "__main__":
    send_feishu()
