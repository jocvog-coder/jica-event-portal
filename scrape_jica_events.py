#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JICA海外協力隊 イベント情報自動集約スクリプト
複数のソースからイベント情報を取得し、統一されたJSON形式で出力
"""

import requests
import json
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
from urllib.parse import urljoin
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JICAEventScraper:
    def __init__(self):
        self.events = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def add_event(self, title, date, time, location, description, category, source_url, source_name):
        """イベント情報を追加"""
        event = {
            'id': len(self.events) + 1,
            'title': title.strip(),
            'date': date,
            'time': time,
            'location': location.strip(),
            'description': description.strip(),
            'category': category,
            'source_url': source_url,
            'source_name': source_name,
            'collected_date': datetime.now().isoformat()
        }
        self.events.append(event)
        logger.info(f"イベント追加: {title}")
    
    def scrape_jica_official(self):
        """JICA公式サイトからイベント情報を取得"""
        logger.info("JICA公式サイトからスクレイピング開始...")
        try:
            # JICA公式のイベント情報ページ
            url = "https://www.jica.go.jp/about/event/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # イベント要素を探す（HTMLの構造に応じて調整が必要）
                event_elements = soup.find_all('div', class_=['event-item', 'news-item', 'l-event'])
                
                for element in event_elements:
                    try:
                        title = element.find('h3', class_=['event-title', 'title'])
                        date_elem = element.find('span', class_=['event-date', 'date'])
                        
                        if title and date_elem:
                            title_text = title.get_text(strip=True)
                            date_text = date_elem.get_text(strip=True)
                            link = element.find('a')
                            source_url = urljoin(url, link.get('href', '')) if link else url
                            
                            self.add_event(
                                title=title_text,
                                date=date_text,
                                time='詳細は公式サイト参照',
                                location='JICA関連施設',
                                description='JICA公式イベント',
                                category='other',
                                source_url=source_url,
                                source_name='JICA公式サイト'
                            )
                    except Exception as e:
                        logger.debug(f"イベント解析エラー: {e}")
                        continue
        except Exception as e:
            logger.error(f"JICA公式サイトスクレイピングエラー: {e}")
    
    def scrape_joca_events(self):
        """JOCA（日本海外協力隊協会）のイベント情報を取得"""
        logger.info("JOCA イベント情報スクレイピング開始...")
        try:
            url = "https://www.joca.or.jp/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # JOCAのイベント情報を探す
                event_elements = soup.find_all('div', class_=['event', 'topics'])
                
                for element in event_elements[:10]:  # 最新10件まで
                    try:
                        title = element.find(['h3', 'h4', 'span'])
                        if title:
                            title_text = title.get_text(strip=True)
                            description = element.find('p')
                            desc_text = description.get_text(strip=True) if description else ''
                            
                            self.add_event(
                                title=title_text,
                                date='日時は公式サイト参照',
                                time='',
                                location='東京都',
                                description=desc_text,
                                category='networking',
                                source_url=url,
                                source_name='JOCA（日本海外協力隊協会）'
                            )
                    except Exception as e:
                        logger.debug(f"JOCA イベント解析エラー: {e}")
                        continue
        except Exception as e:
            logger.error(f"JOCA スクレイピングエラー: {e}")
    
    def scrape_rss_feeds(self):
        """RSS フィードからイベント情報を取得"""
        logger.info("RSS フィード解析開始...")
        
        rss_urls = [
            ('https://www.jica.go.jp/about/event/rss.xml', 'JICA公式RSS'),
        ]
        
        for rss_url, source_name in rss_urls:
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:5]:  # 最新5件
                    if 'event' in entry.get('tags', []) or 'イベント' in entry.get('title', ''):
                        self.add_event(
                            title=entry.get('title', 'イベント'),
                            date=entry.get('published', ''),
                            time='',
                            location='各地',
                            description=entry.get('summary', '')[:200],
                            category='other',
                            source_url=entry.get('link', rss_url),
                            source_name=source_name
                        )
            except Exception as e:
                logger.error(f"RSS フィード解析エラー ({rss_url}): {e}")
    
    def scrape_regional_networks(self):
        """地域別OB・OG会のイベント情報を取得（サンプルデータ）"""
        logger.info("地域別ネットワークデータ追加...")
        
        # 実際の運用では、Facebook API や各地域サイトのスクレイピングを実装
        regional_events = [
            {
                'title': '東京支部 定例会',
                'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                'time': '18:30～20:30',
                'location': '東京都渋谷区',
                'description': '協力隊経験者の交流会です',
                'category': 'networking',
                'source_url': 'https://facebook.com/jica-tokyo-ob',
                'source_name': 'JICA東京支部 OB・OG会'
            },
            {
                'title': '大阪支部 同期会',
                'date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
                'time': '19:00～21:00',
                'location': '大阪府大阪市',
                'description': '同期生の懇親会',
                'category': 'reunion',
                'source_url': 'https://facebook.com/jica-osaka-ob',
                'source_name': 'JICA大阪支部 OB・OG会'
            },
        ]
        
        for event in regional_events:
            self.events.append({
                'id': len(self.events) + 1,
                'title': event['title'],
                'date': event['date'],
                'time': event['time'],
                'location': event['location'],
                'description': event['description'],
                'category': event['category'],
                'source_url': event['source_url'],
                'source_name': event['source_name'],
                'collected_date': datetime.now().isoformat()
            })
            logger.info(f"地域イベント追加: {event['title']}")
    
    def save_to_json(self, output_file='events.json'):
        """イベント情報をJSON形式で保存"""
        try:
            # 日付でソート
            sorted_events = sorted(self.events, key=lambda x: x['date'])
            
            data = {
                'last_updated': datetime.now().isoformat(),
                'total_events': len(sorted_events),
                'events': sorted_events
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSON保存完了: {output_file} ({len(sorted_events)} イベント)")
        except Exception as e:
            logger.error(f"JSON保存エラー: {e}")
    
    def scrape_all(self):
        """すべてのソースからスクレイピングを実行"""
        logger.info("=" * 60)
        logger.info("JICA イベント情報自動集約開始")
        logger.info("=" * 60)
        
        self.scrape_jica_official()
        self.scrape_joca_events()
        self.scrape_rss_feeds()
        self.scrape_regional_networks()
        
        logger.info("=" * 60)
        logger.info(f"合計 {len(self.events)} 件のイベント情報を取得しました")
        logger.info("=" * 60)
        
        return self.events


if __name__ == '__main__':
    scraper = JICAEventScraper()
    scraper.scrape_all()
    scraper.save_to_json('events.json')
