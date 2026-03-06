import os
import requests
from bs4 import BeautifulSoup

# 1. 定義「根源網址」對應表 (根據你的 Markdown 邏輯)
SOURCE_MAP = {
    "原油": "https://www.macromicro.me/collections/13/energy-oil",
    "庫存": "https://www.eia.gov/petroleum/supply/weekly/",
    "通膨": "https://www.macromicro.me/charts/46/us-5-year-breakeven-inflation-rate",
    "黃金": "https://www.macromicro.me/collections/24/precious-metal-gold",
    "糧食": "https://www.macromicro.me/collections/36/agriculture-corn-soybean-wheat",
    "法說會": "https://mops.twse.com.tw/mops/web/t100sb02_1",
    "2330": "https://mops.twse.com.tw/mops/web/t100sb02_1",
    "銅": "https://www.macromicro.me/collections/35/industrial-metal-copper-iron-aluminum"
}

def get_relevant_links(query):
    """根據輸入主題，找出對應的根源連結"""
    links = []
    for key, url in SOURCE_MAP.items():
        if key in query:
            links.append(f"- [{key} 數據根源]({url})")
    return "\n".join(links) if links else "- [通用數據源](https://www.macromicro.me/)"

def ai_analysis(query, raw_data):
    """結合你的三層思考邏輯與數據"""
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    # 注入你的三層思考 Prompt
    prompt = f"""
    主題：{query}
    最新參考資訊：{raw_data[:1000]}
    
    請以『GEM 投資判斷機器人』身份，執行以下分析：
    ### 🎯 核心分析報告
    1. **[第一層：市場直覺]** (描述表面現象與大眾恐慌/樂觀點)
    2. **[第二層：產業實相]** (分析企業痛點、成本轉嫁與補償機制)
    3. **[第三層：供應鏈佈局]** (精確點名台灣受惠/受害類股)
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload)
    return response.json()['candidates'][0]['content']['parts'][0]['text']

if __name__ == "__main__":
    # 假設這是從 GitHub Action 傳入的搜尋主題 (例如：原油通膨)
    query_topic = os.getenv("USER_QUERY", "原油通膨") 
    
    print(f"🔍 正在針對「{query_topic}」進行深度搜尋...")
    
    # 這裡可以加入爬蟲抓取邏輯 (省略細節以保持精簡)
    dummy_data = "偵測到全球通膨預期攀升，原油庫存數據出現異常波動..."
    
    # 執行 AI 分析
    report = ai_analysis(query_topic, dummy_data)
    
    # 取得對應的正確根源連結
    source_links = get_relevant_links(query_topic)
    
    # 寫入 Markdown 報告
    with open("DAILY_REPORT.md", "w", encoding="utf-8") as f:
        f.write(f"# 📅 GEM 投資判斷報告 - 主題：{query_topic}\n\n")
        f.write(report + "\n\n")
        f.write("--- \n### 📡 數據根源與監控網址\n")
        f.write(source_links)
        
    print("✅ 報告已生成，並附上正確根源連結。")
