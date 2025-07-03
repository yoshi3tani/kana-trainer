import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import uuid

# --- ローマ字辞書（正確な表記） ---
romaji_dict = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "o", "ん": "n,m",
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
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "シェ": "she", "チェ": "che", "ジェ": "je",
    "ツァ": "tsa", "ツェ": "tse", "ツォ": "tso",
    "ファ": "fa", "フィ": "fi", "フェ": "fe", "フォ": "fo",
    "ティ": "ti", "ディ": "dhi", "デュ": "dyu",
    "ウィ": "wi", "ウェ": "we", "ウォ": "wo",
    "クォ": "quo", "ヴァ": "va", "ヴィ": "vi", "ヴェ": "ve", "ヴォ": "vo"
}

# --- Utility ---
def to_katakana(text):
    return ''.join([chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ん' else c for c in text])

def generate_audio(char):
    tts = gTTS(text=char, lang='ja')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    uid = str(uuid.uuid4())
    return f"<audio autoplay id='{uid}' controls src='data:audio/mp3;base64,{b64}'></audio>"

# --- Select language ---
lang_labels = {
    "en": {
        "title": "Kana Trainer",
        "subtitle": "Click a kana to hear pronunciation and see romaji.",
        "script": "Script",
        "dakuten": "Dakuten",
        "basic": "Basic only",
        "with_dakuten": "With dakuten",
        "main": "Main Characters",
        "youon": "Youon",
        "foreign": "Foreign Words"
    },
    "ja": {
        "title": "五十音トレーナー",
        "subtitle": "文字をクリックして発音とローマ字を確認。",
        "script": "表記",
        "dakuten": "濁点",
        "basic": "基本のみ",
        "with_dakuten": "濁点を含む",
        "main": "基本文字",
        "youon": "拗音",
        "foreign": "外来語"
    },
    "th": {
        "title": "เทรนเนอร์ตัวอักษรคานะ",
        "subtitle": "แตะตัวอักษรเพื่อฟังเสียงและดูโรมาจิ",
        "script": "สคริปต์",
        "dakuten": "ดะคุเท็น",
        "basic": "พื้นฐานเท่านั้น",
        "with_dakuten": "รวมดะคุเท็น",
        "main": "อักขระหลัก",
        "youon": "เสียงควบ",
        "foreign": "คำต่างประเทศ"
    }
}

lang = st.selectbox("Language / 言語 / ภาษา", ["en", "ja", "th"], index=0)
lbl = lang_labels[lang]

st.title(lbl["title"])
st.write(lbl["subtitle"])

script = st.radio(lbl["script"], ["HIRAGANA", "KATAKANA"])
dakuten = st.radio(lbl["dakuten"], [lbl["basic"], lbl["with_dakuten"]])

# --- Grids ---
base = [
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

extra = [
    ["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"],
    ["だ", "ぢ", "づ", "で", "ど"], ["ば", "び", "ぶ", "べ", "ぼ"],
    ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
    ["きゃ", "", "きゅ", "", "きょ"], ["しゃ", "", "しゅ", "", "しょ"],
    ["ちゃ", "", "ちゅ", "", "ちょ"], ["にゃ", "", "にゅ", "", "にょ"],
    ["ひゃ", "", "ひゅ", "", "ひょ"], ["みゃ", "", "みゅ", "", "みょ"]
]

foreign_words = [
    ["シェ", "チェ", "ジェ"], ["ツァ", "ツェ", "ツォ"],
    ["ファ", "フィ", "フェ", "フォ"], ["ティ", "ディ", "デュ"],
    ["ウィ", "ウェ", "ウォ"], ["クォ"], ["ヴァ", "ヴィ", "ヴェ", "ヴォ"]
]

# --- Display table ---
st.subheader(lbl["main"])
grid = base if dakuten == lbl["basic"] else base + extra
for row in grid:
    cols = st.columns(len(row))
    for i, char in enumerate(row):
        if char == "":
            cols[i].markdown(" ")
            continue
        display_char = to_katakana(char) if script == "KATAKANA" else char
        if cols[i].button(display_char):
            romaji = romaji_dict.get(char, romaji_dict.get(display_char, ""))
            st.markdown(f"**{display_char}** → `{romaji}`")
            st.markdown(generate_audio(display_char), unsafe_allow_html=True)

# --- 外来語表示（カタカナのみ & 濁点あり） ---
if script == "KATAKANA" and dakuten == lbl["with_dakuten"]:
    st.subheader(lbl["foreign"])
    for row in foreign_words:
        cols = st.columns(len(row))
        for i, char in enumerate(row):
            if cols[i].button(char):
                romaji = romaji_dict.get(char, "")
                st.markdown(f"**{char}** → `{romaji}`")
                st.markdown(generate_audio(char), unsafe_allow_html=True)
