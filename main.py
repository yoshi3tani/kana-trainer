import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# --- ローマ字辞書 ---
romaji_dict = {
    # 基本音
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "o", "ん": "n,m",
    # 濁点
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    # 半濁点
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    # 拗音
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
    # 外来語
    "シェ": "she", "チェ": "che", "ジェ": "je",
    "ツァ": "tsa", "ツェ": "tse", "ツォ": "tso",
    "ファ": "fa", "フィ": "fi", "フェ": "fe", "フォ": "fo",
    "ティ": "ti", "ディ": "dhi", "デュ": "dyu",
    "ウィ": "wi", "ウェ": "we", "ウォ": "wo",
    "クォ": "quo",
    "ヴァ": "va", "ヴィ": "vi", "ヴェ": "ve", "ヴォ": "vo",
}

# カタカナ対応
romaji_dict.update({"".join([chr(ord(c)+0x60) for c in k]): v for k, v in romaji_dict.items() if all('ぁ' <= ch <= 'ん' for ch in k)})

def generate_audio(char):
    tts = gTTS(text=char, lang='ja')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    return f"<audio autoplay controls src='data:audio/mp3;base64,{b64}'></audio>"

# ラベル
lang_labels = {
    "ja": {"title": "五十音発音練習アプリ", "basic": "基本", "with_all": "全部", "dakuten": "濁点", "handakuten": "半濁点", "youon": "拗音", "foreign": "外来語"},
    "en": {"title": "Kana Pronunciation Trainer", "basic": "Basic", "with_all": "All", "dakuten": "Voiced", "handakuten": "Semi-voiced", "youon": "Youon", "foreign": "Foreign Words"},
    "th": {"title": "ฝึกการออกเสียงคานะ", "basic": "พื้นฐาน", "with_all": "ทั้งหมด", "dakuten": "เสียงเสริม(ดะคุเท็น)", "handakuten": "เสียงเสริม(ฮันดะคุเท็น)", "youon": "พยางค์ผสม", "foreign": "คำต่างประเทศ"},
}

# 各セクション
basic = [["あ", "い", "う", "え", "お"], ["か", "き", "く", "け", "こ"], ["さ", "し", "す", "せ", "そ"], ["た", "ち", "つ", "て", "と"], ["な", "に", "ぬ", "ね", "の"], ["は", "ひ", "ふ", "へ", "ほ"], ["ま", "み", "む", "め", "も"], ["や", "", "ゆ", "", "よ"], ["ら", "り", "る", "れ", "ろ"], ["わ", "", "を", "", "ん"]]
dakuten = [["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"], ["だ", "ぢ", "づ", "で", "ど"], ["ば", "び", "ぶ", "べ", "ぼ"]]
handakuten = [["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]]
youon = [["きゃ", "きゅ", "きょ"], ["しゃ", "しゅ", "しょ"], ["ちゃ", "ちゅ", "ちょ"], ["にゃ", "にゅ", "にょ"], ["ひゃ", "ひゅ", "ひょ"], ["みゃ", "みゅ", "みょ"], ["りゃ", "りゅ", "りょ"]]
foreign_words = [["シェ", "チェ", "ジェ"], ["ツァ", "ツェ", "ツォ"], ["ファ", "フィ", "フェ", "フォ"], ["ティ", "ディ", "デュ"], ["ウィ", "ウェ", "ウォ"], ["クォ"], ["ヴァ", "ヴィ", "ヴェ", "ヴォ"]]

# 言語とスクリプト選択
lang = st.selectbox("Language / 言語 / ภาษา", ["ja", "en", "th"], format_func=lambda x: lang_labels[x]['title'])
lbl = lang_labels[lang]

st.title(lbl['title'])
script = st.radio("Script", ["HIRAGANA", "KATAKANA"])
mode = st.radio("Mode", [lbl['basic'], lbl['with_all']])

# 表示関数
def display_grid(grid):
    for row in grid:
        cols = st.columns(len(row))
        for i, kana in enumerate(row):
            if not kana: continue
            label = kana if script == "HIRAGANA" else "".join([chr(ord(ch)+0x60) if 'ぁ' <= ch <= 'ん' else ch for ch in kana])
            if cols[i].button(label, key=label):
                romaji = romaji_dict.get(label, "")
                st.markdown(f"**{label}** → `{romaji}`")
                st.markdown(generate_audio(label), unsafe_allow_html=True)

# セクション描画
st.subheader(lbl['basic'])
display_grid(basic)

if mode == lbl['with_all']:
    st.subheader(lbl['dakuten'])
    display_grid(dakuten)

    st.subheader(lbl['handakuten'])
    display_grid(handakuten)

    st.subheader(lbl['youon'])
    display_grid(youon)

    if script == "KATAKANA":
        st.subheader(lbl['foreign'])
        display_grid(foreign_words)
