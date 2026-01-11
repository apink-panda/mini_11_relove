import pandas as pd
import requests
import os
import re
from jinja2 import Environment, FileSystemLoader

import json

from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    },
    'last_updated_label': {
        'TC': '最後更新時間',
        'KR': '마지막 업데이트',
        'EN': 'Last Updated',
        'JP': '最終更新'
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

def fetch_video_dates(video_ids):
    """Fetches publish dates for a list of video IDs using YouTube Data API."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Warning: YOUTUBE_API_KEY not found. Skipping date fetch.")
        return {}

    video_dates = {}
    
    # Process in batches of 50 (YouTube API limit)
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        ids_str = ','.join(batch)
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ids_str}&key={api_key}'
        
        try:
            # Add Referer header to match API Key restrictions
            headers = {'Referer': 'https://apink-panda.com'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    video_dates[item['id']] = item['snippet']['publishedAt']
            else:
                print(f"Error fetching dates: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception fetching dates: {e}")
            
    return video_dates

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

        # Fetch dates and sort
        if data:
            video_ids = [v['id'] for v in data]
            dates_map = fetch_video_dates(video_ids)
            
            for v in data:
                # Add date to video object, default to empty string if not found
                # Format ISO date to YYYY-MM-DD for display if needed, or keep for sorting
                raw_date = dates_map.get(v['id'], '')
                v['publishedAt'] = raw_date[:10] if raw_date else ''
                
            # Sort by publishedAt descending (newest first)
            # Empty dates will be at the end if we use a key that handles them
            # Sort by publishedAt descending (newest first)
            # Empty dates will be at the end if we use a key that handles them
            data.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
            
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

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
    
    # Get current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html_output = template.render(
        sheets=all_videos,
        current_sheet='Love Me More',
        site_title=TRANSLATIONS['site_title']['TC'], # Default to TC
        translations_json=json.dumps(TRANSLATIONS),
        last_updated=current_time
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("Site generated successfully: index.html")

if __name__ == "__main__":
    build_site()
