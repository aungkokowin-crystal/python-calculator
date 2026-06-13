import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

# ---------- State ----------
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "just_evaled" not in st.session_state:
    st.session_state.just_evaled = False

OPS = {"÷": "/", "×": "*", "−": "-", "+": "+"}


# ---------- Database (optional) ----------
def get_conn():
    try:
        return st.connection("history", type="sql")
    except Exception:
        return None


def save_history(expr, result):
    conn = get_conn()
    if conn is None:
        return
    try:
        from sqlalchemy import text
        with conn.session as s:
            s.execute(
                text("INSERT INTO history (expr, result) VALUES (:e, :r)"),
                {"e": str(expr), "r": str(result)},
            )
            s.commit()
    except Exception:
        pass


# ---------- Calculator logic ----------
def press(key):
    e = st.session_state.expr

    if key == "AC":
        st.session_state.expr = ""
        st.session_state.just_evaled = False
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
            save_history(e, val)
            st.session_state.expr = str(val)
            st.session_state.just_evaled = True
        except Exception:
            st.session_state.expr = "Error"
        return

    if st.session_state.just_evaled and key not in OPS:
        e = ""
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


# ---------- iPhone-style CSS ----------
st.markdown(
    """
    <style>
    .stApp { background:#000; }
    .block-container {
        max-width:430px;
        padding:2rem 0.9rem 1rem 0.9rem;
        font-family:-apple-system, BlinkMacSystemFont, "SF Pro Display",
            "Helvetica Neue", Arial, sans-serif;
    }

    /* Display — big, thin, right-aligned, no box (like iPhone) */
    .display {
        color:#fff; text-align:right;
        font-weight:200;
        font-size:clamp(3.6rem, 22vw, 6rem);
        line-height:1.1;
        padding:0 0.4rem 1.2rem 0.4rem;
        min-height:96px;
        overflow-x:auto; white-space:nowrap;
        font-family:-apple-system, BlinkMacSystemFont, "SF Pro Display",
            "Helvetica Neue", Arial, sans-serif;
    }

    /* Rows stay horizontal; tight iPhone spacing */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.55rem !important;
        margin-bottom: 0.55rem;
    }
    div[data-testid="stColumn"], div[data-testid="column"] {
        min-width: 0 !important;
        width: auto !important;
        flex: 1 1 0 !important;
    }

    /* All keys */
    .stButton > button {
        width:100%;
        height:clamp(72px, 19vw, 88px);
        border-radius:999px;
        border:none;
        font-weight:400;
        font-size:clamp(1.9rem, 9vw, 2.5rem);
        padding:0 !important;
        transition:filter .1s ease, transform .06s ease;
        font-family:-apple-system, BlinkMacSystemFont, "SF Pro Display",
            "Helvetica Neue", Arial, sans-serif;
    }
    .stButton > button:active { transform:scale(0.95); }

    /* Digits = dark gray */
    button[kind="secondary"], button[data-testid*="secondary"] {
        background:#333333 !important; color:#fff !important;
    }
    button[kind="secondary"]:hover { background:#737373 !important; color:#fff !important; }

    /* Operators (÷ × − + =) = orange */
    button[kind="primary"], button[data-testid*="primary"] {
        background:#ff9f0a !important; color:#fff !important;
    }
    button[kind="primary"]:hover { filter:brightness(1.12); color:#fff !important; }

    /* Top-row function keys (AC ± %) = light gray, dark text */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="stColumn"]:nth-child(-n+3) button,
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="column"]:nth-child(-n+3) button {
        background:#a5a5a5 !important; color:#000 !important;
    }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="stColumn"]:nth-child(-n+3) button:hover,
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="column"]:nth-child(-n+3) button:hover {
        filter:brightness(1.1); color:#000 !important;
    }

    .footer { text-align:center; margin-top:1.4rem; color:#666;
        font-size:0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Display ----------
shown = st.session_state.expr if st.session_state.expr else "0"
st.markdown(f'<div class="display">{shown}</div>', unsafe_allow_html=True)

# ---------- Keypad (iPhone layout) ----------
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

# Row 5: 0 (wide) . =
r5 = st.columns([2, 1, 1])
r5[0].button("0", key="0", on_click=press, args=("0",), use_container_width=True)
r5[1].button(".", key="dot", on_click=press, args=(".",), use_container_width=True)
r5[2].button("=", key="eq", type="primary", on_click=press, args=("=",), use_container_width=True)

# ---------- History ----------
conn = get_conn()
if conn is not None:
    try:
        rows = conn.query(
            "SELECT expr, result, created_at FROM history "
            "ORDER BY created_at DESC LIMIT 15",
            ttl=0,
        )
        with st.expander(f"📜 History ({len(rows)})", expanded=False):
            if len(rows) == 0:
                st.caption("မှတ်တမ်း မရှိသေးပါ")
            for _, row in rows.iterrows():
                st.markdown(f"**{row['expr']} = {row['result']}**")
    except Exception as ex:
        st.error(f"⚠️ History error:\n\n{type(ex).__name__}: {ex}")

# ---------- Footer ----------
st.markdown('<div class="footer">Developed by AKKW</div>', unsafe_allow_html=True)
