import pandas as pd
import streamlit as st
import base64
import random

st.set_page_config(page_title="クイズに正解してまむこに奪われたお金を取り戻そう", layout="centered")
st.markdown("## クイズに正解してまむこに奪われたお金を取り戻そう")

if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_order" not in st.session_state:
    df = pd.read_excel("クイズ.xlsx")
    st.session_state.quiz_order = random.sample(range(len(df)), len(df))
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "play_sound" not in st.session_state:
    st.session_state.play_sound = None

def load_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f"""
        <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """

# 効果音再生
if st.session_state.play_sound == "correct":
    st.markdown(load_audio("ojisan_game_assets/charin.mp3"), unsafe_allow_html=True)
elif st.session_state.play_sound == "wrong":
    st.markdown(load_audio("ojisan_game_assets/18_macho_damage.wav"), unsafe_allow_html=True)
elif st.session_state.play_sound == "clear":
    st.markdown(load_audio("ojisan_game_assets/fanfare.mp3"), unsafe_allow_html=True)
st.session_state.play_sound = None

st.markdown(f"### 💰 現在の回収額：{st.session_state.score} 円")

# クリア判定
if st.session_state.score >= 5000:
    st.success("🎉 クリア！まむこから5,000円を取り戻した！")
    st.markdown(load_audio("ojisan_game_assets/fanfare.mp3"), unsafe_allow_html=True)  
    st.balloons()
    st.session_state.play_sound = "clear"

    if st.button("🔁 もう一度まむこをしばく！"):
        st.session_state.score = 0
        st.session_state.quiz_index = 0
        st.session_state.quiz_order = random.sample(range(len(pd.read_excel("クイズ.xlsx"))), len(pd.read_excel("クイズ.xlsx")))
        st.session_state.show_result = False
        st.rerun()
    st.stop()

# クイズ出題
df = pd.read_excel("クイズ.xlsx")
if st.session_state.quiz_index < len(st.session_state.quiz_order):
    idx = st.session_state.quiz_order[st.session_state.quiz_index]
    row = df.iloc[idx]

    st.markdown("---")
    st.markdown(f"**❓ 問題：{row['question']}**")
    col1, col2 = st.columns(2)

    def answer_chosen(choice):
        correct = row["answer"]
        if choice == correct:
            st.session_state.score += 2000
            st.session_state.last_result = "✅ 正解！2,000円回収した！"
            st.session_state.play_sound = "correct"
        else:
            st.session_state.score -= 1000
            st.session_state.last_result = "❌ 不正解！まむこに1,000円奪われた…"
            st.session_state.play_sound = "wrong"
        st.session_state.quiz_index += 1
        st.session_state.show_result = True
        st.rerun()

    with col1:
        if st.button(row["option_1"]):
            answer_chosen(row["option_1"])
    with col2:
        if st.button(row["option_2"]):
            answer_chosen(row["option_2"])

# 結果表示
if st.session_state.show_result:
    if "不正解" in st.session_state.last_result:
        st.image("ojisan_game_assets/ojisan.png", use_container_width=True)
    st.info(st.session_state.last_result)
    st.session_state.show_result = False
