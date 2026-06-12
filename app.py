import streamlit as st

# ---------- Page setup ----------
st.set_page_config(
    page_title="AKKW Calculator",
    page_icon="🧮",
    layout="centered",
)

# ---------- Custom styling ----------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Glass card container */
    .block-container {
        max-width: 640px;
        padding-top: 2.5rem;
    }

    /* Title */
    .calc-title {
        text-align: center;
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    .calc-sub {
        text-align: center;
        color: #e6e6ff;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    /* Card */
    .glass {
        background: rgba(255,255,255,0.95);
        border-radius: 22px;
        padding: 1.8rem 1.8rem 1.2rem 1.8rem;
        box-shadow: 0 18px 45px rgba(0,0,0,0.30);
    }

    /* Inputs */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 0;
        margin-top: 0.5rem;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
        box-shadow: 0 6px 18px rgba(245,87,108,0.45);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(245,87,108,0.55);
        color: white;
    }

    /* Result box */
    .result-box {
        margin-top: 1.4rem;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 16px;
        padding: 1.3rem;
        text-align: center;
        font-size: 1.7rem;
        font-weight: 800;
        box-shadow: 0 8px 22px rgba(17,153,142,0.45);
    }
    .result-err {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        box-shadow: 0 8px 22px rgba(235,51,73,0.45);
        font-size: 1.2rem;
    }

    /* Footer credit */
    .footer {
        text-align: center;
        margin-top: 2.2rem;
        color: #ffffff;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    .footer .name {
        font-weight: 800;
        background: linear-gradient(90deg,#ffd86f,#fc6262);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<div class="calc-title">🧮 AKKW Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="calc-sub">လွယ်ကူလျင်မြန်သော Web ဂဏန်းတွက်စက်</div>', unsafe_allow_html=True)

# ---------- Calculator card ----------
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("ပထမဂဏန်း", value=0.0)
    with col2:
        num2 = st.number_input("ဒုတိယဂဏန်း", value=0.0)

    operation = st.selectbox(
        "တွက်ချက်မည့် ပုံစံ",
        ["ပေါင်းရန် (+)", "နုတ်ရန် (-)", "မြှောက်ရန် (×)", "စားရန် (÷)"],
    )

    calculate = st.button("🎯  တွက်ချက်မည်")

    if calculate:
        error = False
        if operation == "ပေါင်းရန် (+)":
            result = num1 + num2
        elif operation == "နုတ်ရန် (-)":
            result = num1 - num2
        elif operation == "မြှောက်ရန် (×)":
            result = num1 * num2
        else:  # စားရန် (÷)
            if num2 != 0:
                result = num1 / num2
            else:
                result = "⚠️ သုညဖြင့် စား၍မရပါ"
                error = True

        box_class = "result-box result-err" if error else "result-box"
        display = result if error else f"ရလဒ် = {result:,.4g}"
        st.markdown(
            f'<div class="{box_class}">{display}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer">Developed by <span class="name">AKKW</span> 💜</div>',
    unsafe_allow_html=True,
)
