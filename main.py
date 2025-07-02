### Streamlit version: Interactive Kana Pronunciation Trainer (Responsive UI)
import streamlit as st
from gtts import gTTS
import base64

# --- ローマ字辞書（正確な表記） ---
romaji_dict = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "さ": "sa", "し": "si", "す": "su", "せ": "se", "そ": "so",
    "ざ": "za", "じ": "zi", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "た": "ta", "ち": "ti", "つ": "tu", "て": "te", "と": "to",
    "だ": "da", "ぢ": "di", "づ": "du", "で": "de", "ど": "do",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "hu", "へ": "he", "ほ": "ho",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo", "ん": "n",
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo"
}

gojuon_basic = [
    ["あ", "い", "う", "え", "お"],
    ["か", "き", "く", "け", "こ"],
    ["さ", "し", "す", "せ", "そ"],
    ["た", "ち", "つ", "て", "と"],
    ["な", "に", "ぬ", "ね", "の"],
    ["は", "ひ", "ふ", "へ", "ほ"],
    ["ま", "み", "む", "め", "も"],
    ["や", "", "ゆ", "", "よ"],
    ["ら", "り", "る", "れ", "ろ"],
    ["わ", "", "を", "", "ん"]
]

gojuon_dakuten = gojuon_basic + [
    ["が", "ぎ", "ぐ", "げ", "ご"],
    ["ざ", "じ", "ず", "ぜ", "ぞ"],
    ["だ", "ぢ", "づ", "で", "ど"],
    ["ば", "び", "ぶ", "べ", "ぼ"],
    ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]
]

youon_filtered = [
    ["きゃ", "", "きゅ", "", "きょ"],
    ["ぎゃ", "", "ぎゅ", "", "ぎょ"],
    ["しゃ", "", "しゅ", "", "しょ"],
    ["じゃ", "", "じゅ", "", "じょ"],
    ["ちゃ", "", "ちゅ", "", "ちょ"],
    ["にゃ", "", "にゅ", "", "にょ"],
    ["ひゃ", "", "ひゅ", "", "ひょ"],
    ["びゃ", "", "びゅ", "", "びょ"],
    ["ぴゃ", "", "ぴゅ", "", "ぴょ"],
    ["みゃ", "", "みゅ", "", "みょ"],
    ["りゃ", "", "りゅ", "", "りょ"]
]

def to_katakana(text):
    return ''.join([chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ん' else c for c in text])

"""
def generate_audio(char):
    tts = gTTS(text=char, lang='ja')
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"<audio autoplay controls src='data:audio/mp3;base64,{b64}'></audio>"
"""
# 代わりに仮の文字列を返す（デバッグ目的）
def generate_audio(char):
    return "(Audio playback disabled in debug mode)"

# --- 多言語UI辞書 ---
lang_labels = {
    "en": {
        "title": "Interactive Kana Pronunciation Trainer",
        "subtitle": "Click a kana to hear the pronunciation and see the romaji.",
        "script": "Script",
        "dakuten": "Dakuten",
        "basic": "Basic only",
        "with_dakuten": "With dakuten",
        "main": "Main Characters",
        "youon": "Youon"
    },
    "ja": {
        "title": "五十音発音練習アプリ",
        "subtitle": "文字をクリックすると発音とローマ字が表示されます。",
        "script": "表記",
        "dakuten": "濁点",
        "basic": "基本のみ",
        "with_dakuten": "濁点を含む",
        "main": "基本文字",
        "youon": "拗音"
    },
    "th": {
        "title": "แอปฝึกการออกเสียงคานะ",
        "subtitle": "แตะที่ตัวอักษรคานะเพื่อฟังการออกเสียงและดูโรมาจิ",
        "script": "สคริปต์",
        "dakuten": "ดะคุเท็น",
        "basic": "เฉพาะพื้นฐาน",
        "with_dakuten": "รวมดะคุเท็นด้วย",
        "main": "ตัวอักษรหลัก",
        "youon": "เสียงพยางค์รวม"
    }
}

# --- 言語選択を上部中央に配置 ---
lang = st.selectbox("Language / 言語 / ภาษา", ["en", "ja", "th"], index=0)
lbl = lang_labels[lang]

st.title(lbl["title"])
st.write(lbl["subtitle"])

script = st.radio(lbl["script"], ["HIRAGANA", "KATAKANA"])
dakuten = st.radio(lbl["dakuten"], [lbl["basic"], lbl["with_dakuten"]])

# --- レイアウト調整 ---
grid = gojuon_dakuten if dakuten == lbl["with_dakuten"] else gojuon_basic

st.subheader(lbl["main"])
for row in grid:
    cols = st.columns(len(row))
    for i, char in enumerate(row):
        if char == "":
            cols[i].markdown(" ")
            continue
        label = to_katakana(char) if script == "KATAKANA" else char
        if cols[i].button(label):
            romaji = romaji_dict.get(char, "")
            st.markdown(f"**{char}** → `{romaji}`")
            st.markdown(generate_audio(char), unsafe_allow_html=True)

if dakuten == lbl["with_dakuten"]:
    st.subheader(lbl["youon"])
    for row in youon_filtered:
        cols = st.columns(len(row))
        for i, char in enumerate(row):
            if char == "":
                cols[i].markdown(" ")
                continue
            label = to_katakana(char) if script == "KATAKANA" else char
            if cols[i].button(label):
                romaji = romaji_dict.get(char, "")
                st.markdown(f"**{char}** → `{romaji}`")
                st.markdown(generate_audio(char), unsafe_allow_html=True)
