# Apink Mini 11 《RE:LOVE》 Comeback Archive 🐼

[![Auto Build](https://github.com/apink-panda/mini_11_relove/actions/workflows/build.yml/badge.svg)](https://github.com/apink-panda/mini_11_relove/actions/workflows/build.yml)
[![Live Site](https://img.shields.io/badge/Live-Demo-brightgreen)](https://apink-panda.github.io/mini_11_relove/)

> [!IMPORTANT]
> **本專案為粉絲自製內容，僅供社群交流分享，嚴禁任何形式之商業營利用途。**
> **This project is a fan-made creation for community sharing only. COMMERCIAL USE IS STRICTLY PROHIBITED.**

這是一個專為 Apink 第 11 張迷你專輯《RE:LOVE》回歸打造的全自動化 **YouTube 影音整理平台**。本專案結合了自動化開發流程與國際化設計，旨在為全球 Panda 提供最即時、最完整的補檔體驗。

## 🌟 核心特色 (Core Features)

*   **⚡️ 全自動化維護 (100% Automated Workflow)**
    *   **無後端架構**：以 Google Sheets 作為輕量化 CMS，實現隨時隨地連結更新。
    *   **CI/CD 自動建置**：整合 GitHub Actions，從更新試算表到網頁上線僅需不到 2 分鐘。
    *   **自動化資料補全**：利用 YouTube Data API 自動抓取影片標題、封面圖與發佈日期，將人工維護成本降至最低。
*   **🌍 國際化支援 (Global i18n Support)**
    *   支援 **繁中、韓、英、日** 四語系即時切換。
    *   整合 Cloudflare 全球加速，確保各國粉絲皆能高速存取。
*   **🎬 互動式影音體驗 (Advanced UX)**
    *   **Multiview Player**：自研多視角同步播放器，支援多個 FanCam 與舞台同步觀看。
    *   **智慧排序**：自動依據影片發佈時間排序，並可自由切換新舊次序。

## 📊 專案影響力 (Performance & Reach)

在回歸啟動後的黃金兩週內，本專案取得了亮眼的社群成效與國際觸及數據：

### 社群數據單次最高 (Social Engagement)
*   **X (Twitter)**: **7,534** 次查看量 | **88** 次轉發 | **57** 個書籤 | **147** 個愛心
*   **Threads**: **3,054** 次瀏覽量 | **14** 次轉發

### 流量分布 (Traffic via Cloudflare)
本專案成功觸及全球多個語系市場，總瀏覽量逾 **17,200+** 次：

| 國家/地區 (Region) | 瀏覽量 (Traffic) | 比率 (%) |
| :--- | :--- | :--- |
| **Taiwan (台灣)** | 5,566 | ~32% |
| **Japan (日本)** | 3,947 | ~23% |
| **France (法國)** | 3,176 | ~18% |
| **Hong Kong (香港)** | 2,627 | ~15% |
| **United States (美國)** | 2,092 | ~12% |

## 🛠 技術堆疊 (Tech Stack)

*   **Frontend**: Vanilla HTML/JS, CSS (Glassmorphism design)
*   **Backend/Generator**: Python (Pandas, Jinja2)
*   **Automation**: GitHub Actions (CI/CD)
*   **API Integration**: YouTube Data API v3, YouTube oEmbed, YouTube IFrame API
*   **Deployment**: GitHub Pages + Cloudflare

---

## ⚠️ 免責聲明與授權 (Disclaimer & License)

*   **Content**: This repository is for non-commercial fan creation purposes only. All video content and IP belong to their respective owners (IST Entertainment, etc.).
*   **Code**: The source code of this project is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](./LICENSE).
    *   **姓名標示 (BY)**：使用或修改程式碼時請標註原作者。
    *   **非商業性 (NC)**：禁止任何營利用途。
    *   **相同方式分享 (SA)**：衍生作品必須以同等授權開源。
