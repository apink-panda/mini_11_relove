import pandas as pd
import requests
import os
import re
from jinja2 import Environment, FileSystemLoader

import json

# Configuration
SHEET_ID = '1YN3_ehOl7SPNXnxn5ob7j6GAcrRF00W-4seatqcSQEY'
SHEETS = {
    'Love Me More': '0',
    'Sunshine': '1164317946',
    'Hold My Hand': '761520964',
    '經典歌曲': '1115179049',
    '訪問': '1065948851',
    '應援': '1456843045',
}

TRANSLATIONS = {
    'site_title': {
        'TC': 'Apink 回歸整理',
        'KR': '에이핑크 컴백 정리',
        'EN': 'Apink Comeback Archive',
        'JP': 'Apink カムバックまとめ'
    },
    'tabs': {
        'Love Me More': {'TC': 'Love Me More', 'KR': 'Love Me More', 'EN': 'Love Me More', 'JP': 'Love Me More'},
        'Sunshine': {'TC': 'Sunshine', 'KR': 'Sunshine', 'EN': 'Sunshine', 'JP': 'Sunshine'},
        'Hold My Hand': {'TC': 'Hold My Hand', 'KR': 'Hold My Hand', 'EN': 'Hold My Hand', 'JP': 'Hold My Hand'},
        '經典歌曲': {'TC': '經典歌曲', 'KR': '명곡', 'EN': 'Classic Songs', 'JP': '名曲'},
        '訪問': {'TC': '訪問', 'KR': '인터뷰/예능', 'EN': 'Interview', 'JP': 'インタビュー'},
        '應援': {'TC': '應援', 'KR': '응원법', 'EN': 'Fanchant', 'JP': '応援'}
    }
}

def get_video_id(url):
    """Extracts YouTube Video ID from a URL."""
    if pd.isna(url): return None
    url = str(url).strip()
    # Handle various YouTube URL formats
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    return match.group(1) if match else None

def fetch_data(sheet_id, gid='0'):
    """Fetches CSV data from Google Sheets."""
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    try:
        print(f"Fetching data from {url}...")
        df = pd.read_csv(url, header=None) # Assuming no header based on preview, or maybe first row is header?
        # Looking at previous output: 
        # https://www.youtube.com/watch?v=iL0jeKQqQNk,[4K] Apink “Love me more” Band LIVE [it's Live] 現場音樂表演
        # It seems row 1 is data, not header.
        
        # Let's clean it up
        data = []
        for _, row in df.iterrows():
            video_url = row[0]
            title = row[1] if len(row) > 1 else "Unknown Title"
            
            vid_id = get_video_id(video_url)
            if vid_id:
                data.append({
                    'id': vid_id,
                    'url': f'https://www.youtube.com/watch?v={vid_id}',
                    'title': str(title).strip(),
                    'thumbnail': f'https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg' # High quality thumb: maxresdefault
                })
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def build_site():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
def get_all_videos():
    """Fetches videos for all sheets."""
    all_videos = {}
    for sheet_name, gid in SHEETS.items():
        videos = fetch_data(SHEET_ID, gid)
        all_videos[sheet_name] = videos
        print(f"Found {len(videos)} videos for '{sheet_name}'")
    return all_videos

def build_site():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
    all_videos = get_all_videos()
    
    html_output = template.render(
        sheets=all_videos,
        current_sheet='Love Me More',
        site_title=TRANSLATIONS['site_title']['TC'], # Default to TC
        translations_json=json.dumps(TRANSLATIONS)
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("Site generated successfully: index.html")

if __name__ == "__main__":
    build_site()
