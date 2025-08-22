# main.py — Kana Pronunciation Trainer (Japanese only)
import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# ===============================
# 音声（gTTS → <audio autoplay>）
# ===============================
@st.cache_data(show_spinner=False, max_entries=512)
def tts_b64(text: str, lang_code: str) -> str:
    tts = gTTS(text=text, lang=lang_code)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return base64.b64encode(fp.read()).decode()

def speak(text: str, lang_code: str = "ja"):
    if not text or not text.strip():
        return
    try:
        b64 = tts_b64(text, lang_code)
        st.markdown(
            f"<audio autoplay controls src='data:audio/mp3;base64,{b64}'></audio>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning("音声の生成に失敗しました。ネットワーク状況をご確認ください。")
        st.caption(f"details: {e}")

# ===============================
# UI ラベル（学習対象は日本語のみ）
# ===============================
LABELS = {
    "ja": {
        "app_title": "かな 発音トレーナー（日本語）",
        "ui_lang": "UI 言語",
        "script": "スクリプト",
        "hiragana": "HIRAGANA",
        "katakana": "KATAKANA",
        "jp_scope_title": "表示モード",
        "jp_scope_basic": "基本のみ",
        "jp_scope_all": "全部",
        "section_basic": "基本（あ〜ん）",
        "section_dakuten": "濁点",
        "section_handakuten": "半濁点",
        "section_youon": "拗音（濁音・半濁点含む）",
        "section_foreign": "外来語（カタカナのみ）",
        "cols_title": "レイアウト調整（スマホで崩れる場合は列数↓）",
        "cols_label": "ボタン列数",
    },
    "en": {
        "app_title": "Kana Pronunciation Trainer (Japanese)",
        "ui_lang": "UI Language",
        "script": "Script",
        "hiragana": "HIRAGANA",
        "katakana": "KATAKANA",
        "jp_scope_title": "Display mode",
        "jp_scope_basic": "Basic only",
        "jp_scope_all": "All",
        "section_basic": "Basic (a–n rows)",
        "section_dakuten": "Voiced (dakuten)",
        "section_handakuten": "Semi-voiced (handakuten)",
        "section_youon": "Youon (incl. voiced/semi-voiced)",
        "section_foreign": "Foreign (Katakana only)",
        "cols_title": "Layout (reduce columns on phones)",
        "cols_label": "Buttons per row",
    },
    "th": {
        "app_title": "ตัวอักษรคานะ ฝึกออกเสียง (ภาษาญี่ปุ่น)",
        "ui_lang": "ภาษา UI",
        "script": "สคริปต์",
        "hiragana": "ฮิรางานะ",
        "katakana": "คาตากานะ",
        "jp_scope_title": "โหมดแสดงผล",
        "jp_scope_basic": "พื้นฐานเท่านั้น",
        "jp_scope_all": "ทั้งหมด",
        "section_basic": "พื้นฐาน (あ〜ん)",
        "section_dakuten": "ดะคุเท็น",
        "section_handakuten": "ฮันดะคุเท็น",
        "section_youon": "พยางค์ผสม (รวมเสียงก้อง/ฮันดะคุเท็น)",
        "section_foreign": "คำยืม (เฉพาะคาตากานะ)",
        "cols_title": "การจัดวาง (ถ้าเละบนมือถือให้ลดจำนวนคอลัมน์)",
        "cols_label": "จำนวนปุ่มต่อแถว",
    },
}

# ===============================
# ローマ字辞書（＋カタカナ対応）
# ===============================
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
    # 拗音（清音）
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    # 拗音（濁音・半濁点）※「ぢゃ系」は含めない
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja",  "じゅ": "ju",  "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    # 外来語（カタカナ見出しあり）
    "シェ": "she", "チェ": "che", "ジェ": "je",
    "ツァ": "tsa", "ツェ": "tse", "ツォ": "tso",
    "ファ": "fa", "フィ": "fi", "フェ": "fe", "フォ": "fo",
    "ティ": "ti", "ディ": "dhi", "デュ": "dyu",
    "ウィ": "wi", "ウェ": "we", "ウォ": "wo",
    "クォ": "quo",
    "ヴァ": "va", "ヴィ": "vi", "ヴェ": "ve", "ヴォ": "vo",
}
# カタカナ対応（ひらがな→カタカナ）
romaji_dict.update({
    "".join([chr(ord(c)+0x60) for c in k]): v
    for k, v in romaji_dict.items()
    if all('ぁ' <= ch <= 'ん' for ch in k)
})

# ===============================
# 表示データ
# ===============================
basic = [
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
dakuten = [["が", "ぎ", "ぐ", "げ", "ご"], ["ざ", "じ", "ず", "ぜ", "ぞ"], ["だ", "ぢ", "づ", "で", "ど"], ["ば", "び", "ぶ", "べ", "ぼ"]]
handakuten = [["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]]
# 拗音（※「ぢゃ・ぢゅ・ぢょ」は含めない）
youon = [
    ["きゃ", "きゅ", "きょ"],
    ["ぎゃ", "ぎゅ", "ぎょ"],
    ["しゃ", "しゅ", "しょ"],
    ["じゃ", "じゅ", "じょ"],
    ["ちゃ", "ちゅ", "ちょ"],
    ["にゃ", "にゅ", "にょ"],
    ["ひゃ", "ひゅ", "ひょ"],
    ["びゃ", "びゅ", "びょ"],
    ["ぴゃ", "ぴゅ", "ぴょ"],
    ["みゃ", "みゅ", "みょ"],
    ["りゃ", "りゅ", "りょ"],
]
foreign_words = [["シェ", "チェ", "ジェ"], ["ツァ", "ツェ", "ツォ"], ["ファ", "フィ", "フェ", "フォ"], ["ティ", "ディ", "デュ"], ["ウィ", "ウェ", "ウォ"], ["クォ"], ["ヴァ", "ヴィ", "ヴェ", "ヴォ"]]

# ===============================
# ヘルパー
# ===============================
def render_kana_grid(grid, script_label: str, key_prefix: str = "ja"):
    for r, row in enumerate(grid):
        cols = st.columns(len(row))
        for c, kana in enumerate(row):
            if not kana:
                continue
            label = kana if script_label == "HIRAGANA" else "".join(
                [chr(ord(ch)+0x60) if 'ぁ' <= ch <= 'ん' else ch for ch in kana]
            )
            if cols[c].button(label, key=f"{key_prefix}-{script_label}-{r}-{c}-{label}"):
                roma = romaji_dict.get(label, "")
                st.markdown(f"**{label}** → `{roma}`")
                speak(label, "ja")

# ===============================
# UI
# ===============================
ui = st.selectbox("UI / 言語 / ภาษา", ["ja", "en", "th"], index=0,
                  format_func=lambda k: LABELS[k]["app_title"])
L = LABELS[ui]
st.title(L["app_title"])

# レイアウト調整（1〜10列、URLクエリ ?cols=1 等に対応）
with st.expander(L["cols_title"], expanded=False):
    qp = st.query_params
    raw = qp.get("cols", "4")
    if isinstance(raw, list):
        raw = raw[0]
    try:
        default_cols = max(1, min(10, int(raw)))
    except Exception:
        default_cols = 4
    cols_per_row = st.slider(L["cols_label"], min_value=1, max_value=10, value=default_cols, step=1)
    st.query_params["cols"] = str(cols_per_row)

# スクリプト選択 & 表示モード
script = st.radio(L["script"], [L["hiragana"], L["katakana"]], index=0, horizontal=True)
jp_scope = st.radio(L["jp_scope_title"], [L["jp_scope_basic"], L["jp_scope_all"]],
                    index=0, horizontal=True)

# 基本
st.subheader(L["section_basic"])
render_kana_grid(basic, "HIRAGANA" if script == L["hiragana"] else "KATAKANA", key_prefix="ja-basic")

# 全部の場合のみ以下を追加
if jp_scope == L["jp_scope_all"]:
    st.subheader(L["section_dakuten"])
    render_kana_grid(dakuten, "HIRAGANA" if script == L["hiragana"] else "KATAKANA", key_prefix="ja-daku")

    st.subheader(L["section_handakuten"])
    render_kana_grid(handakuten, "HIRAGANA" if script == L["hiragana"] else "KATAKANA", key_prefix="ja-handaku")

    st.subheader(L["section_youon"])
    render_kana_grid(youon, "HIRAGANA" if script == L["hiragana"] else "KATAKANA", key_prefix="ja-youon")

    if script == L["katakana"]:
        st.subheader(L["section_foreign"])
        render_kana_grid(foreign_words, "KATAKANA", key_prefix="ja-foreign")
