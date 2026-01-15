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
    'Winning': '2037301453',
    'Love Me More': '0',
    'Sunshine': '1164317946',
    'Hold My Hand': '761520964',
    '經典歌曲': '1115179049',
    '訪問': '1065948851',
    '應援': '1456843045',
    'Apink Diary': '807890805',
}

TRANSLATIONS = {
    'site_title': {
        'TC': 'Apink 回歸整理',
        'KR': '에이핑크 컴백 정리',
        'EN': 'Apink Comeback Archive',
        'JP': 'Apink カムバックまとめ'
    },
    'tabs': {
        'Winning': {'TC': '一位', 'KR': '1위', 'EN': 'No.1', 'JP': '1位'},
        'Love Me More': {'TC': 'Love Me More', 'KR': 'Love Me More', 'EN': 'Love Me More', 'JP': 'Love Me More'},
        'Sunshine': {'TC': 'Sunshine', 'KR': 'Sunshine', 'EN': 'Sunshine', 'JP': 'Sunshine'},
        'Hold My Hand': {'TC': 'Hold My Hand', 'KR': 'Hold My Hand', 'EN': 'Hold My Hand', 'JP': 'Hold My Hand'},
        '經典歌曲': {'TC': '經典歌曲', 'KR': '명곡', 'EN': 'Classic Songs', 'JP': '名曲'},
        '訪問': {'TC': '訪問', 'KR': '인터뷰/예능', 'EN': 'Interview', 'JP': 'インタビュー'},
        '應援': {'TC': '應援', 'KR': '응원법', 'EN': 'Fanchant', 'JP': '応援'},
        'Apink Diary': {'TC': 'Apink Diary', 'KR': 'Apink Diary', 'EN': 'Apink Diary', 'JP': 'Apink Diary'}
    },
    'last_updated_label': {
        'TC': '最後更新時間',
        'KR': '마지막 업데이트',
        'EN': 'Last Updated',
        'JP': '最終更新'
    },
    'about_tooltip': {
        'TC': '關於這個網站',
        'KR': '이 사이트에 대하여',
        'EN': 'About this site',
        'JP': 'このサイトについて'
    },
    'about_back_home': {
        'TC': '← 回到首頁',
        'KR': '← 홈으로 돌아가기',
        'EN': '← Back to Home',
        'JP': '← ホームに戻る'
    },
    'about_article_title': {
        'TC': '[技術分享] 為了 Apink 回歸！如何在一天內打造全自動更新的 YT 整理網站',
        'KR': '[기술 공유] 에이핑크 컴백을 위해! 하루 만에 전자동 업데이트 YT 정리 사이트 만드는 법',
        'EN': '[Tech Share] For Apink Comeback! Build an Auto-Updating YT Archive in One Day',
        'JP': '[技術共有] Apinkカムバックのために！1日で全自動更新のYTまとめサイトを作る方法'
    },
    'about_preface_title': {
        'TC': '前言：迷妹/迷弟的極限開發',
        'KR': '서론: 팬의 극한 개발',
        'EN': 'Preface: Extreme Development by a Fan',
        'JP': 'はじめに：ファンの限界開発'
    },
    'about_preface_p1': {
        'TC': '作為一個 Panda (Apink 粉絲)，看到 Apink 帶著 Mini 11《RELOVE》回歸，心情激動之餘，也發現大量的物料（MV、Live 舞台、綜藝、電台、應援法）散落在 YouTube 各處。為了讓大家能更方便地補檔，我決定做一個整理網站。',
        'KR': '판다(에이핑크 팬)로서 에이핑크가 Mini 11 《RELOVE》로 컴백하는 것을 보고 감격스러운 마음과 함께, 수많은 자료(MV, 라이브 무대, 예능, 라디오, 응원법)가 유튜브 곳곳에 흩어져 있는 것을 발견했습니다. 모두가 편하게 찾아볼 수 있도록 정리 사이트를 만들기로 결심했습니다.',
        'EN': 'As a Panda (Apink fan), witnessing Apink\'s comeback with Mini 11 "RELOVE" was thrilling. However, I noticed that tons of content (MVs, live stages, variety shows, radio, fanchants) were scattered across YouTube. To make it easier for everyone to keep up, I decided to create an archive site.',
        'JP': 'Panda（Apinkのファン）として、ApinkがMini 11「RELOVE」でカムバックするのを見て感激すると同時に、膨大な資料（MV、ライブ、バラエティ、ラジオ、応援法）がYouTubeのあち口に散らばっていることに気づきました。みんなが簡単にチェックできるように、まとめサイトを作ることにしました。'
    },
    'about_preface_p2': {
        'TC': '但問題是：我只有不到一天的時間。回歸期每一分每一秒都很珍貴，我不能花太多時間在寫扣上，但又希望網站能自動更新、介面好看。',
        'KR': '하지만 문제는 시간이 하루도 채 남지 않았다는 것이었습니다. 컴백 기간의 매 순간이 소중하기에 코딩에 너무 많은 시간을 할애할 수 없었지만, 사이트가 자동으로 업데이트되고 디자인도 예쁘길 바랐습니다.',
        'EN': 'The challenge was: I had less than a day. Every second during the comeback is precious. I couldn\'t spend too much time coding, yet I wanted the site to update automatically and look great.',
        'JP': 'しかし問題は、1日も時間がないということでした。カムバック期間の1分1秒が惜しいため、コーディングに時間をかけすぎるわけにはいきませんでしたが、サイトが自動更新され、デザインも綺麗であることを望んでいました。'
    },
    'about_preface_p3': {
        'TC': '這篇文章將分享我如何利用 Python + Google Sheets + GitHub Actions，在一天內快速搭建出一個自動化、低成本且易於維護的偶像回歸整理站。',
        'KR': '이 글에서는 Python + Google Sheets + GitHub Actions를 이용해 하루 만에 자동화되고 유지보수가 쉬운 아이돌 컴백 정리 사이트를 구축한 경험을 공유합니다.',
        'EN': 'This article shares how I used Python + Google Sheets + GitHub Actions to quickly build an automated, low-cost, and easy-to-maintain comeback archive in a single day.',
        'JP': 'この記事では、Python + Google Sheets + GitHub Actionsを利用して、1日で自動化され、低コストでメンテナンスが容易なアイドルカムバックまとめサイトをスピード構築した方法を共有します。'
    },
    'about_arch_title': {
        'TC': '核心架構：什麼最快？',
        'KR': '핵심 구조: 무엇이 가장 빠른가?',
        'EN': 'Core Architecture: What\'s Fastest?',
        'JP': 'コアアーキテクチャ：何が最速か？'
    },
    'about_arch_p1': {
        'TC': '為了追求極致的開發速度與最低的維護成本，我選擇了以下的「非典型」技術堆疊：',
        'KR': '최고의 개발 속도와 최저의 유지보수 비용을 위해 다음과 같은 "비전형적인" 기술 스택을 선택했습니다:',
        'EN': 'To achieve maximum development speed and minimum maintenance cost, I chose the following "non-traditional" tech stack:',
        'JP': '究極の開発スピードと最低のメンテナンスコストを追求するために、以下の「非典型的」な技術スタックを選択しました：'
    },
    'about_arch_li1': {
        'TC': 'CMS (內容管理系統) -> Google Sheets - 沒有比 Excel/Sheets 更直覺的後台了。手機也能編輯，方便隨時隨地新增影片網址。',
        'KR': 'CMS (콘텐츠 관리 시스템) -> Google Sheets - Excel/Sheets보다 직관적인 백엔드는 없습니다. 모바일에서도 편집이 가능해 언제 어디서나 영상을 추가할 수 있습니다.',
        'EN': 'CMS (Content Management System) -> Google Sheets - There\'s no backend more intuitive than Excel/Sheets. It can be edited via phone, making it easy to add video URLs anytime, anywhere.',
        'JP': 'CMS (コンテンツ管理システム) -> Google Sheets - Excel/Sheetsほど直感的な管理画面はありません。スマホでも編集可能で、いつでもどこでも動画URLを追加できます。'
    },
    'about_arch_li2': {
        'TC': '後端/建置 -> Python (Pandas + Jinja2) - Python 處理資料最強。用 Pandas 讀取 Sheets，用 Jinja2 產生 HTML。',
        'KR': '백엔드/빌드 -> Python (Pandas + Jinja2) - Python은 데이터 처리에 가장 강력합니다. Pandas로 Sheets를 읽고 Jinja2로 HTML을 생성합니다.',
        'EN': 'Backend/Build -> Python (Pandas + Jinja2) - Python is king for data processing. Use Pandas to read Sheets and Jinja2 to generate HTML.',
        'JP': 'バックエンド/ビルド -> Python (Pandas + Jinja2) - Pythonはデータ処理に最強です。PandasでSheetsを読み込み、Jinja2でHTMLを生成します。'
    },
    'about_arch_li3': {
        'TC': '資料庫 -> 無 (Static Site) - 靜態網頁最快，免費託管選擇多（GitHub Pages, Vercel 等）。',
        'KR': '데이터베이스 -> 없음 (Static Site) - 정적 웹사이트가 가장 빠르며 GitHub Pages, Vercel 등 무료 호스팅 옵션이 많습니다.',
        'EN': 'Database -> None (Static Site) - Static sites are the fastest, with many free hosting options like GitHub Pages or Vercel.',
        'JP': 'データベース -> なし (Static Site) - 静的サイトが最速で、GitHub PagesやVercelなど無料のホスティング先も豊富です。'
    },
    'about_arch_li4': {
        'TC': '自動化 -> GitHub Actions - 只要我更新 Google Sheets，觸發 Action，它就自動跑 Python 腳本更新網頁並 Push 回去。',
        'KR': '자동화 -> GitHub Actions - Google Sheets를 업데이트하고 Action을 트리거하면 자동으로 Python 스크립트가 실행되어 웹페이지를 업데이트하고 다시 Push합니다.',
        'EN': 'Automation -> GitHub Actions - Just update Google Sheets, trigger the Action, and it automatically runs the Python script to update the site and push it back.',
        'JP': '自動化 -> GitHub Actions - Google Sheetsを更新してActionをトリガーするだけで、Pythonスクリプトが自動実行され、サイトを更新してPushし直します。'
    },
    'about_tech_title': {
        'TC': '技術實作細節',
        'KR': '기술 구현 상세',
        'EN': 'Technical Implementation Details',
        'JP': '技術実装の詳細'
    },
    'about_tech_s1_title': {
        'TC': '1. Google Sheets 當作簡易資料庫',
        'KR': '1. Google Sheets를 간이 데이터베이스로 사용',
        'EN': '1. Google Sheets as a Simple Database',
        'JP': '1. Google Sheetsを簡易データベースとして利用'
    },
    'about_tech_s1_p1': {
        'TC': '我建立了一個 Google Sheet，裡面有好幾個分頁（Tab），分別對應「主打歌」、「收錄曲」、「綜藝」等分類。欄位只需要一個「YouTube 連結」和選填的「標題」。',
        'KR': '여러 개의 탭으로 구성된 Google Sheet를 만들어 "타이틀곡", "수록곡", "예능" 등의 카테고리를 나누었습니다. 필드는 "유튜브 링크"와 선택 사항인 "제목"만 있으면 됩니다.',
        'EN': 'I created a Google Sheet with multiple tabs corresponding to categories like "Title Song," "B-sides," "Variety," etc. Each only needs a "YouTube Link" and an optional "Title" field.',
        'JP': '「タイトル曲」「収録曲」「バラエティ」などの各カテゴリーに対応した複数のタブを持つGoogle Sheetを作成しました。項目は「YouTubeリンク」と任意入力の「タイトル」だけです。'
    },
    'about_tech_s1_p2': {
        'TC': '在程式碼中，我直接使用 Sheets 的 CSV 輸出功能，不需要申請複雜的 Google API 權限，只要公開試算表即可：',
        'KR': '코드에서는 Sheets의 CSV 출력 기능을 직접 사용하여 복잡한 Google API 권한 신청 없이 시트만 공개하면 됩니다.',
        'EN': 'In the code, I use the Sheets CSV export feature directly, avoiding complex Google API setups. Just make the sheet public.',
        'JP': 'プログラム内では、SheetsのCSV出力機能を直接利用しているため、複雑なGoogle APIの権限設定は不要で、スプレッドシートを公開するだけで済みます。'
    },
    'about_tech_s2_title': {
        'TC': '2. 自動抓取 YouTube 資訊 (省去手動輸入)',
        'KR': '2. 유튜브 정보 자동 수집 (수동 입력 생략)',
        'EN': '2. Automatic YouTube Info Scraping (No Manual Input)',
        'JP': '2. YouTube情報の自動取得（手動入力の省略）'
    },
    'about_tech_s2_p1': {
        'TC': '為了讓整理更輕鬆，我不想手動複製貼上影片標題和發布日期。所以我接了 YouTube Data API 和 oEmbed。',
        'KR': '정리를 더 쉽게 하기 위해 영상 제목과 게시 날짜를 일일이 복사해서 붙여넣고 싶지 않았습니다. 그래서 YouTube Data API와 oEmbed를 연결했습니다.',
        'EN': 'To simplify things, I didn\'t want to manually copy-paste video titles and dates. So, I integrated YouTube Data API and oEmbed.',
        'JP': '整理を楽にするために、動画のタイトルや投稿日をいちいちコピペしたくなかったので、YouTube Data APIとoEmbedを連携させました。'
    },
    'about_tech_s2_li1': {
        'TC': '標題：利用 oEmbed 介面，不需要 API Key 也能抓到標題。',
        'KR': '제목: oEmbed 인터페이스를 이용해 API Key 없이도 제목을 가져올 수 있습니다.',
        'EN': 'Title: Use the oEmbed interface to fetch titles without an API Key.',
        'JP': 'タイトル：oEmbedインターフェースを利用することで、APIキーなしでもタイトルを取得できます。'
    },
    'about_tech_s2_li2': {
        'TC': '日期：為了做「按時間排序」的功能，我使用 YouTube Data API 批次抓取影片的 publishedAt。',
        'KR': '날짜: "시간순 정렬" 기능을 위해 YouTube Data API를 사용하여 영상의 publishedAt을 일괄 수집합니다.',
        'EN': 'Date: For the "Sort by Date" feature, I use the YouTube Data API to batch-fetch publishedAt timestamps.',
        'JP': '日付：「時間順ソート」機能のために、YouTube Data APIを使って動画のpublishedAtを一括取得します。'
    },
    'about_tech_s2_p2': {
        'TC': '這樣我只需要在 Excel 貼上網址，標題和日期都會由程式自動補完。',
        'KR': '이렇게 하면 엑셀에 URL만 붙여넣으면 제목과 날짜가 프로그램에 의해 자동으로 완성됩니다.',
        'EN': 'This way, I only need to paste the URL in Excel, and the program fills in the title and date.',
        'JP': 'これにより、ExcelにURLを貼るだけで、タイトルと日付がプログラムによって自動的に補完されます。'
    },
    'about_tech_s3_title': {
        'TC': '3. 靜態網頁生成 (SSG)',
        'KR': '3. 정적 사이트 생성 (SSG)',
        'EN': '3. Static Site Generation (SSG)',
        'JP': '3. 静的サイト生成 (SSG)'
    },
    'about_tech_s3_p1': {
        'TC': '雖然現在有 Next.js / Nuxt 這些強大的框架，但對於這種單頁應用，寫一個簡單的 Python Script 搭配 Jinja2 模板是最快的。',
        'KR': 'Next.js나 Nuxt 같은 강력한 프레임워크가 많지만, 이런 단일 페이지 애플리케이션에는 Jinja2 템플릿과 함께 간단한 Python 스크립트를 쓰는 것이 가장 빠릅니다.',
        'EN': 'While powerful frameworks like Next.js or Nuxt exist, a simple Python script with Jinja2 templates is fastest for this kind of single-page app.',
        'JP': 'Next.jsやNuxtなどの強力なフレームワークもありますが、このようなシングルページアプリケーションには、Jinja2テンプレートとシンプルなPythonスクリプトを組み合わせるのが最速です。'
    },
    'about_tech_s3_p2': {
        'TC': '流程如下：',
        'KR': '절차는 다음과 같습니다:',
        'EN': 'The flow is as follows:',
        'JP': 'フローは次の通りです：'
    },
    'about_tech_s3_li1': {
        'TC': 'Python 跑蟲把資料抓下來整理成 JSON 物件。',
        'KR': 'Python 크롤러가 데이터를 가져와 JSON 객체로 정리합니다.',
        'EN': 'Python script fetches data and organizes it into JSON objects.',
        'JP': 'Pythonスクリプトがデータを取得し、JSONオブジェクトに整理します。'
    },
    'about_tech_s3_li2': {
        'TC': '將資料倒進 index.html 的 Jinja2 模板。',
        'KR': '데이터를 index.html의 Jinja2 템플릿에 주입합니다.',
        'EN': 'Inject data into the index.html Jinja2 template.',
        'JP': 'データをindex.htmlのJinja2テンプレートに流し込みます。'
    },
    'about_tech_s3_li3': {
        'TC': '輸出最終的 index.html。',
        'KR': '최종 index.html을 출력합니다.',
        'EN': 'Export the final index.html.',
        'JP': '最終的なindex.htmlを出力します。'
    },
    'about_tech_s4_title': {
        'TC': '4. GitHub Actions 實現 CI/CD',
        'KR': '4. GitHub Actions를 통한 CI/CD 구현',
        'EN': '4. CI/CD with GitHub Actions',
        'JP': '4. GitHub ActionsによるCI/CDの実現'
    },
    'about_tech_s4_p1': {
        'TC': '這是最關鍵的一步。我寫了一個 Workflow，每當我 Push Code 或是手動觸發時，它會：',
        'KR': '가장 중요한 단계입니다. 코드 푸시나 수동 트리거 시 실행되는 워크플로우를 작성했습니다:',
        'EN': 'This is the most critical step. I wrote a workflow that runs whenever I push code or trigger it manually:',
        'JP': 'これが最も重要なステップです。コードのプッシュや手動トリガー時に実行されるワークフローを作成しました：'
    },
    'about_tech_s4_li1': {
        'TC': 'Check out 程式碼。',
        'KR': '코드를 체크아웃합니다.',
        'EN': 'Check out the code.',
        'JP': 'コードをチェックアウトします。'
    },
    'about_tech_s4_li2': {
        'TC': '安裝 Python 環境。',
        'KR': 'Python 환경을 설치합니다.',
        'EN': 'Set up Python environment.',
        'JP': 'Python環境をセットアップします。'
    },
    'about_tech_s4_li3': {
        'TC': '執行 build.py (抓新資料 -> 產出新 HTML)。',
        'KR': 'build.py를 실행합니다 (새 데이터 수집 -> 새 HTML 생성).',
        'EN': 'Run build.py (fetch new data -> generate new HTML).',
        'JP': 'build.pyを実行します（新データ取得 -> 新HTML生成）。'
    },
    'about_tech_s4_li4': {
        'TC': '將變更的 index.html Commit 並 Push 回儲存庫。',
        'KR': '변경된 index.html을 커밋하고 저장소에 다시 푸시합니다.',
        'EN': 'Commit changed index.html and push back to the repository.',
        'JP': '変更されたindex.htmlをコミットし、リポジトリにプッシュし直します。'
    },
    'about_tech_s4_p2': {
        'TC': '這樣一來，網站隨時保持最新，而且完全不用手動去 deploy。',
        'KR': '덕분에 웹사이트는 항상 최신 상태를 유지하며 수동 배포가 전혀 필요 없습니다.',
        'EN': 'This ensures the site stays up-to-date without any manual deployment.',
        'JP': 'これにより、サイトは常に最新の状態に保たれ、手動でのデプロイは一切不要になります。'
    },
    'about_highlight_title': {
        'TC': '前端亮點：多語系與簡單互動',
        'KR': '프론트엔드 하이라이트: 다국어 및 간단한 상호작용',
        'EN': 'Frontend Highlights: Multi-language & Simple Interaction',
        'JP': 'フロントエンドの見どころ：多言語とシンプルな操作'
    },
    'about_highlight_p1': {
        'TC': '前端部分保持簡單，使用了 Vanilla JS (原生 JavaScript)。特別加了一個功能：多語系切換 (繁中/韓/英/日)，讓海外粉絲也能使用。這是透過一個簡單的 JS 字典替換 DOM 文字實現的。',
        'KR': '프론트엔드는 Vanilla JS(순수 자바스크립트)를 사용해 심플함을 유지했습니다. 특히 해외 팬들도 사용할 수 있게 다국어 전환(번체 중문/한국어/영어/일본어) 기능을 추가했습니다. 이는 간단한 JS 딕셔너리로 DOM 텍스트를 교체하는 방식으로 구현되었습니다.',
        'EN': 'The frontend remains simple using Vanilla JS. We added a multi-language switcher (TC/KR/EN/JP) so international fans can use it. This is implemented via a simple JS dictionary replacing DOM text.',
        'JP': 'フロントエンドはシンプルに保ち、Vanilla JS（純粋なJavaScript）を使用しました。特に海外ファンも利用できるように、多言語切り替え（繁体中国語/韓国語/英語/日本語）機能を追加しました。これはシンプルなJS辞書でDOMのテキストを置き換えることで実現されています。'
    },
    'about_result_title': {
        'TC': '成果與心得',
        'KR': '결과 및 소감',
        'EN': 'Results and Thoughts',
        'JP': '成果と感想'
    },
    'about_result_p1': {
        'TC': '這套系統的優點在於：',
        'KR': '이 시스템의 장점은 다음과 같습니다:',
        'EN': 'The advantages of this system are:',
        'JP': 'このシステムの利点は以下の通りです：'
    },
    'about_result_li1': {
        'TC': '快：開發快，讀取快（純靜態檔）。',
        'KR': '빠름: 개발이 빠르고 로딩이 빠릅니다 (순수 정적 파일).',
        'EN': 'Fast: Quick development and fast loading (pure static files).',
        'JP': '速い：開発が速く、読み込みも速い（純粋な静的ファイル）。'
    },
    'about_result_li2': {
        'TC': '省：完全免費（GitHub Actions + Google Sheets）。',
        'KR': '절약: 완전 무료입니다 (GitHub Actions + Google Sheets).',
        'EN': 'Cost-effective: Completely free (GitHub Actions + Google Sheets).',
        'JP': '節約：完全無料（GitHub Actions + Google Sheets）。'
    },
    'about_result_li3': {
        'TC': '懶：更新資料只需要動手指貼連結到 Google Sheets。',
        'KR': '편함: 구글 시트에 링크만 붙여넣으면 데이터가 업데이트됩니다.',
        'EN': 'Convenient: Just paste links into Google Sheets to update data.',
        'JP': '楽：Google Sheetsにリンクを貼るだけでデータが更新されます。'
    },
    'about_result_p2': {
        'TC': '不到一天的時間，就完成了一個能自動排列時間、支援多語系、視覺風格符合此次回歸概念（粉黑配色）的整理站。',
        'KR': '하루도 안 되는 시간에 자동 시간 정렬, 다국어 지원, 이번 컴백 컨셉(핑크&블랙)에 맞춘 디자인의 정리 사이트를 완성했습니다.',
        'EN': 'In less than a day, I completed an archive site that auto-sorts by time, supports multiple languages, and matches the visual style of this comeback (pink and black).',
        'JP': '1日足らずで、自動時間ソート、多言語対応、今回のカムバックコンセプト（ピンク＆ブラック）に合わせたデザインのまとめサイトを完成させました。'
    },
    'about_result_p3': {
        'TC': '對於想要快速整理資訊並分享給社群的工程師來說，這套「Google Sheets + Python SSG + GitHub Actions」的組合拳，絕對是 CP 值最高的選擇！',
        'KR': '정보를 빠르게 정리해 커뮤니티와 공유하고 싶은 개발자에게 "Google Sheets + Python SSG + GitHub Actions" 조합은 최고의 가성비를 자랑하는 선택입니다!',
        'EN': 'For engineers who want to quickly organize and share info with the community, this "Google Sheets + Python SSG + GitHub Actions" combo is definitely the best choice!',
        'JP': '情報を素早く整理してコミュニティに共有したいエンジニアにとって、「Google Sheets + Python SSG + GitHub Actions」の組み合わせは、間違いなくコスパ最強の選択肢です！'
    },
    'about_fighting': {
        'TC': 'Apink FIGHTING! RELOVE 大發！',
        'KR': '에이핑크 파이팅! RELOVE 대박!',
        'EN': 'Apink FIGHTING! RELOVE Success!',
        'JP': 'Apink ファイティン！ RELOVE 大ヒット！'
    },
    'badge_first_win': {
        'TC': '獲得一位',
        'KR': '1위',
        'EN': '1st Win',
        'JP': '1位獲得'
    }
}

def get_video_id(url):
    """Extracts YouTube Video ID from a URL."""
    if pd.isna(url): return None
    url = str(url).strip()
    # Handle various YouTube URL formats
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    match = re.search(regex, url)
    return match.group(1) if match else None

def fetch_youtube_title(video_url):
    """Fetches video title using YouTube oEmbed."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
        response = requests.get(oembed_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('title')
    except Exception as e:
        print(f"Error fetching title for {video_url}: {e}")
    return None

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
        # https://www.youtube.com/watch?v=iL0jeKQqQNk,[4K] Apink "Love me more" Band LIVE [it's Live] 現場音樂表演
        # It seems row 1 is data, not header.
        
        # Let's clean it up
        data = []
        for _, row in df.iterrows():
            video_url = row[0]
            # Check if title exists in CSV
            if len(row) > 1 and not pd.isna(row[1]) and str(row[1]).strip() != '':
                title = str(row[1]).strip()
            else:
                # Fetch from YouTube if missing
                print(f"Fetching title for {video_url}...")
                fetched_title = fetch_youtube_title(video_url)
                title = fetched_title if fetched_title else "Unknown Title"
            
            vid_id = get_video_id(video_url)
            
            if vid_id:
                video_data = {
                    'id': vid_id,
                    'url': f'https://www.youtube.com/watch?v={vid_id}',
                    'title': str(title).strip(),
                    'thumbnail': f'https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg' # High quality thumb: maxresdefault
                }
                data.append(video_data)

        # Fetch dates and sort
        if data:
            video_ids = [v['id'] for v in data]
            dates_map = fetch_video_dates(video_ids)
            
            for v in data:
                # Add date to video object, default to empty string if not found
                # Format ISO date to YYYY-MM-DD for display if needed, or keep for sorting
                raw_date = dates_map.get(v['id'], '')
                v['publishedAt'] = raw_date  # Keep full ISO string for accurate sorting
                v['displayDate'] = raw_date[:10] if raw_date else ''
                
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

def group_videos_by_date(videos):
    """Groups a list of videos by their displayDate."""
    groups = {}
    for video in videos:
        date = video.get('displayDate', 'Unknown Date')
        if date not in groups:
            groups[date] = []
        groups[date].append(video)
    
    # Convert to list of objects for template, sorted by date descending
    # (Assuming dates are YYYY-MM-DD, string sort works)
    sorted_dates = sorted(groups.keys(), reverse=True)
    
    grouped_list = []
    for date in sorted_dates:
        grouped_list.append({
            'date': date,
            'videos': groups[date]
        })
    return grouped_list

def build_site():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
    all_videos = get_all_videos()
    
    # Group videos for each sheet
    grouped_videos = {}
    for sheet, videos in all_videos.items():
        grouped_videos[sheet] = group_videos_by_date(videos)
    
    # Get current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    version_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    html_output = template.render(
        sheets=grouped_videos,
        current_sheet='Winning',
        site_title=TRANSLATIONS['site_title']['TC'], # Default to TC
        translations_json=json.dumps(TRANSLATIONS),
        translations_dict=TRANSLATIONS,
        last_updated=current_time,
        version=version_timestamp
    )
    
    about_template = env.get_template('about.html')
    about_html = about_template.render(
        site_title=TRANSLATIONS['site_title']['TC'],
        version=version_timestamp
    )
    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(about_html)
    print("Site generated successfully: about.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("Site generated successfully: index.html")

if __name__ == "__main__":
    build_site()
