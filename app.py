import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="AKKW Calculator", page_icon="🧮", layout="centered")

# ---------- State ----------
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "just_evaled" not in st.session_state:
    st.session_state.just_evaled = False

OPS = {"÷": "/", "×": "*", "−": "-", "+": "+"}


def press(key):
    e = st.session_state.expr

    if key == "AC":
        st.session_state.expr = ""
        st.session_state.just_evaled = False
        return

    if key == "⌫":
        st.session_state.expr = e[:-1]
        return

    if key == "±":
        if e and e[0] == "-":
            st.session_state.expr = e[1:]
        elif e:
            st.session_state.expr = "-" + e
        return

    if key == "%":
        try:
            st.session_state.expr = str(float(eval(_safe(e))) / 100)
        except Exception:
            pass
        return

    if key == "=":
        try:
            val = eval(_safe(e))
            if val == int(val):
                val = int(val)
            st.session_state.expr = str(val)
            st.session_state.just_evaled = True
        except Exception:
            st.session_state.expr = "Error"
        return

    # digit / dot / operator
    if st.session_state.just_evaled and key not in OPS:
        e = ""  # start fresh after a result if a number is pressed
    st.session_state.just_evaled = False
    if e == "Error":
        e = ""
    st.session_state.expr = e + key


def _safe(e):
    for k, v in OPS.items():
        e = e.replace(k, v)
    if not e or any(c not in "0123456789.+-*/() " for c in e):
        raise ValueError("bad")
    return e


# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp { background:#000; }
    .block-container {
        max-width:420px;
        padding-top:1.2rem;
        padding-left:0.6rem; padding-right:0.6rem;
    }

    .calc-head { text-align:center; color:#fff; font-weight:800;
        font-size:1.4rem; margin-bottom:0.5rem; }

    /* Display */
    .display {
        background:#1c1c1e; border-radius:20px;
        padding:1.3rem 1.2rem;
        text-align:right; color:#fff;
        font-size:clamp(2rem, 9vw, 3rem); font-weight:300;
        min-height:80px; line-height:1.2; margin-bottom:0.8rem;
        overflow-x:auto; word-break:break-all;
        box-shadow: inset 0 0 0 1px #2c2c2e;
    }

    /* Keep the 4-button rows horizontal on mobile (Streamlit stacks them by default) */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
    }
    div[data-testid="stColumn"], div[data-testid="column"] {
        min-width: 0 !important;
        width: auto !important;
        flex: 1 1 0 !important;
    }

    /* Buttons — responsive circular keys */
    .stButton > button {
        width:100%;
        height:clamp(84px, 25vw, 130px);
        border-radius:50%; border:none;
        font-size:clamp(2.6rem, 12vw, 3.4rem); font-weight:600;
        padding:0 !important;
        transition:filter .12s ease, transform .08s ease;
    }
    .stButton > button:active { transform:scale(0.94); }

    /* Digits = dark gray */
    button[kind="secondary"], button[data-testid*="secondary"] {
        background:#333 !important; color:#fff !important;
    }
    button[kind="secondary"]:hover, button[data-testid*="secondary"]:hover {
        filter:brightness(1.3); color:#fff !important;
    }
    /* Operators = orange */
    button[kind="primary"], button[data-testid*="primary"] {
        background:#ff9500 !important; color:#fff !important;
    }
    button[kind="primary"]:hover, button[data-testid*="primary"]:hover {
        filter:brightness(1.1); color:#fff !important;
    }

    .footer { text-align:center; margin-top:1.4rem; color:#888;
        font-size:0.9rem; }
    .footer .name { font-weight:800; color:#ff9500; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header + display ----------
st.markdown('<div class="calc-head">🧮 AKKW Calculator</div>', unsafe_allow_html=True)

shown = st.session_state.expr if st.session_state.expr else "0"
st.markdown(f'<div class="display">{shown}</div>', unsafe_allow_html=True)

# ---------- Keypad ----------
# Row 1: AC ± % ÷
r1 = st.columns(4)
r1[0].button("AC", key="AC", on_click=press, args=("AC",), use_container_width=True)
r1[1].button("±", key="pm", on_click=press, args=("±",), use_container_width=True)
r1[2].button("%", key="pc", on_click=press, args=("%",), use_container_width=True)
r1[3].button("÷", key="div", type="primary", on_click=press, args=("÷",), use_container_width=True)

# Row 2: 7 8 9 ×
r2 = st.columns(4)
for i, d in enumerate(["7", "8", "9"]):
    r2[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r2[3].button("×", key="mul", type="primary", on_click=press, args=("×",), use_container_width=True)

# Row 3: 4 5 6 −
r3 = st.columns(4)
for i, d in enumerate(["4", "5", "6"]):
    r3[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r3[3].button("−", key="sub", type="primary", on_click=press, args=("−",), use_container_width=True)

# Row 4: 1 2 3 +
r4 = st.columns(4)
for i, d in enumerate(["1", "2", "3"]):
    r4[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r4[3].button("+", key="add", type="primary", on_click=press, args=("+",), use_container_width=True)

# Row 5: ⌫ 0 . =
r5 = st.columns(4)
r5[0].button("⌫", key="back", on_click=press, args=("⌫",), use_container_width=True)
r5[1].button("0", key="0", on_click=press, args=("0",), use_container_width=True)
r5[2].button(".", key="dot", on_click=press, args=(".",), use_container_width=True)
r5[3].button("=", key="eq", type="primary", on_click=press, args=("=",), use_container_width=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer">Developed by <span class="name">AKKW</span></div>',
    unsafe_allow_html=True,
)
