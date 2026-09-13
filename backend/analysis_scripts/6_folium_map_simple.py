"""
脚本6简化版：Folium交互地图 - 6_folium_map_simple.py
使用简单配置，确保地图能正常显示
"""

import folium
from folium.plugins import HeatMap, Fullscreen
import pandas as pd
from config import *

# 方言问候语
GREETINGS = {
    '你吃饭了吗？': '日常问候',
    '今天天气不错呀': '天气评论',
    '你好，欢迎来到这里': '欢迎语',
    '最近过得怎么样？': '关心问候'
}

# 方言介绍
DIALECT_INTRO = {
    '北京官话': '北京官话是现代标准汉语（普通话）的基础方言，主要分布在北京及周边地区。',
    '冀鲁官话': '冀鲁官话分布于河北、山东大部分地区，是华北地区的主要方言。',
    '东北官话': '东北官话是中国使用人口最多的方言之一，分布于东北三省及内蒙古东部。',
    '胶辽官话': '胶辽官话分布于山东半岛和辽东半岛。',
    '中原官话': '中原官话分布于河南、陕西、甘肃等地，是古代中原雅言的继承者。',
    '兰银官话': '兰银官话分布于甘肃、宁夏一带。',
    '江淮官话': '江淮官话分布于江苏、安徽的长江以北地区。',
    '西南官话': '西南官话覆盖四川、重庆、云南、贵州等省市，使用范围最广。',
    '晋语': '晋语是中国北方唯一保留入声的方言，主要分布于山西省。',
    '吴语': '吴语是中国最古老的方言之一，保留了大量中古汉语特征。',
    '湘语': '湘语又称湖南话，主要分布于湖南省。',
    '赣语': '赣语又称江西话，主要分布于江西省。',
    '客家话': '客家话保留了较多唐宋汉语特征，分布于广东、福建、江西等地。',
    '粤语': '粤语保留了完整的中古汉语声调系统，主要分布于广东、广西和港澳地区。',
    '闽语': '闽语是汉语方言中最复杂的一支，内部差异极大。',
    '徽语': '徽语又称徽州话，主要分布于安徽南部。',
    '平话': '平话是广西地区的一种汉语方言。'
}

def load_data():
    df = pd.read_csv(CLEANED_POINTS_FILE, encoding='utf-8-sig')
    return df

def get_marker_color(endanger_level):
    colors = {
        '安全': 'green',
        '较安全': 'blue',
        '脆弱': 'orange',
        '濒危': 'red'
    }
    return colors.get(endanger_level, 'gray')

def get_dialect_intro(dialect_area):
    for key in DIALECT_INTRO:
        if key in dialect_area:
            return DIALECT_INTRO[key]
    return '该方言区暂无详细介绍。'

def create_popup_content(row):
    dialect_intro = get_dialect_intro(row['dialect_area'])
    
    audio_html = """
    <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
        <strong>🎙️ 语音:</strong><br>
    """
    for greeting, label in GREETINGS.items():
        audio_html += f"""
        <button onclick="playAudio('{greeting}')" 
                style="width: 100%; margin: 2px 0; padding: 4px; background: #4a90d9; color: white; border: none; border-radius: 4px; cursor: pointer;">
            {label}: {greeting}
        </button>
        """
    
    audio_html += """
    <script>
    function playAudio(text) {
        if ('speechSynthesis' in window) {
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'zh-CN';
            utterance.rate = 0.8;
            speechSynthesis.speak(utterance);
        } else {
            alert('您的浏览器不支持语音合成');
        }
    }
    </script>
    </div>
    """
    
    content = f"""
    <div style="width: 280px;">
        <h3 style="margin: 0 0 10px 0; color: #4a90d9;">🏮 {row['city']}</h3>
        
        <div style="background: #f8f9fa; padding: 8px; border-radius: 6px; margin-bottom: 8px;">
            <strong>📍 方言区:</strong> {row['dialect_area']}<br>
            <strong>省份:</strong> {row['province']}
        </div>
        
        <div style="background: #e8f4fd; padding: 8px; border-radius: 6px; margin-bottom: 8px;">
            <strong>📊 使用人口:</strong> {row['population_10k']} 万人<br>
            <strong>年轻人使用率:</strong> {row['youth_usage_rate']:.2%}<br>
            <strong>濒危等级:</strong> <span style="color: {'green' if row['endanger_level']=='安全' else 'blue' if row['endanger_level']=='较安全' else 'orange' if row['endanger_level']=='脆弱' else 'red'};">{row['endanger_level']}</span>
        </div>
        
        <div style="background: #fff3cd; padding: 8px; border-radius: 6px; margin-bottom: 8px;">
            <strong>📖 方言介绍</strong><br>
            {dialect_intro}
        </div>
        
        {audio_html}
    </div>
    """
    
    return content

def main():
    print("=" * 60)
    print("脚本6简化版：Folium交互地图")
    print("=" * 60)
    
    print("\n[步骤1] 读取数据...")
    df = load_data()
    
    print("\n[步骤2] 创建地图...")
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
    
    print("\n[步骤3] 添加热力图层...")
    heat_data = [[row['latitude'], row['longitude'], row['endanger_index']] 
                 for idx, row in df.iterrows()]
    HeatMap(heat_data, name='濒危指数热力图', opacity=0.5).add_to(m)
    
    print("\n[步骤4] 添加方言点标记...")
    for idx, row in df.iterrows():
        color = get_marker_color(row['endanger_level'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(create_popup_content(row), max_width=320),
            zindex_offset=1000
        ).add_to(m)
    
    print("\n[步骤5] 添加控制按钮...")
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)
    
    print("\n[步骤6] 保存地图...")
    m.save(DIALECT_MAP_FILE)
    print(f"   已保存: {DIALECT_MAP_FILE}")
    
    print("\n" + "=" * 60)
    print("Folium交互地图创建完成！")
    print("=" * 60)
    
    return m

if __name__ == "__main__":
    main()