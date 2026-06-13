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


# ---------- 3D / framed CSS (smaller) ----------
st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at 50% 0%, #2a2a30 0%, #0a0a0c 70%); }

    /* Calculator BODY = frame + 3D float */
    .block-container {
        max-width: 330px;
        margin-top: 1.4rem;
        padding: 1.1rem 0.95rem 1.3rem 0.95rem !important;
        background: linear-gradient(160deg, #2c2c30 0%, #161618 100%);
        border: 2px solid #3c3c42;
        border-radius: 34px;
        box-shadow:
            0 22px 55px rgba(0,0,0,0.75),
            0 4px 10px rgba(0,0,0,0.5),
            inset 0 1px 1px rgba(255,255,255,0.10),
            inset 0 -2px 4px rgba(0,0,0,0.4);
        font-family:-apple-system, BlinkMacSystemFont, "SF Pro Display",
            "Helvetica Neue", Arial, sans-serif;
    }

    /* Display — recessed (inset) screen */
    .display {
        color:#fff; text-align:right; font-weight:200;
        font-size:clamp(2.4rem, 14vw, 3.6rem);
        line-height:1.1;
        padding:0.8rem 0.9rem;
        min-height:64px; margin-bottom:0.8rem;
        overflow-x:auto; white-space:nowrap;
        background: linear-gradient(160deg, #0b0b0d, #1b1b1e);
        border: 1px solid #2d2d32;
        border-radius: 16px;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.85),
                    inset 0 -1px 1px rgba(255,255,255,0.05);
        font-family:inherit;
    }

    /* Rows */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.45rem !important;
        margin-bottom: 0.45rem;
    }
    div[data-testid="stColumn"], div[data-testid="column"] {
        min-width: 0 !important; width: auto !important; flex: 1 1 0 !important;
    }

    /* Base keys — smaller + 3D raised */
    .stButton > button {
        width:100%;
        height:clamp(52px, 15vw, 64px);
        border-radius:999px;
        border:1px solid rgba(255,255,255,0.06);
        font-weight:500;
        font-size:clamp(1.3rem, 6.2vw, 1.7rem);
        padding:0 !important;
        transition:all .08s ease;
        font-family:inherit;
    }
    .stButton > button:active { transform:translateY(2px) scale(0.97); }

    /* Digits = dark gray, 3D */
    button[kind="secondary"], button[data-testid*="secondary"] {
        background: linear-gradient(145deg, #404044, #28282b) !important;
        color:#fff !important;
        box-shadow: 4px 4px 9px rgba(0,0,0,0.6),
                    -3px -3px 7px rgba(255,255,255,0.05) !important;
    }
    button[kind="secondary"]:active {
        box-shadow: inset 3px 3px 7px rgba(0,0,0,0.7),
                    inset -2px -2px 5px rgba(255,255,255,0.05) !important;
    }

    /* Operators = orange, 3D */
    button[kind="primary"], button[data-testid*="primary"] {
        background: linear-gradient(145deg, #ffb849, #f88a00) !important;
        color:#fff !important;
        box-shadow: 4px 4px 9px rgba(0,0,0,0.5),
                    -3px -3px 7px rgba(255,255,255,0.18) !important;
    }
    button[kind="primary"]:active {
        box-shadow: inset 3px 3px 7px rgba(180,90,0,0.7),
                    inset -2px -2px 5px rgba(255,255,255,0.2) !important;
    }

    /* Function keys (AC ± %) = light gray, 3D */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="stColumn"]:nth-child(-n+3) button,
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="column"]:nth-child(-n+3) button {
        background: linear-gradient(145deg, #c3c3c3, #8f8f8f) !important;
        color:#000 !important;
        box-shadow: 4px 4px 9px rgba(0,0,0,0.5),
                    -3px -3px 7px rgba(255,255,255,0.3) !important;
    }
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="stColumn"]:nth-child(-n+3) button:active,
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
        div[data-testid="column"]:nth-child(-n+3) button:active {
        box-shadow: inset 3px 3px 7px rgba(0,0,0,0.4),
                    inset -2px -2px 5px rgba(255,255,255,0.4) !important;
    }

    .footer { text-align:center; margin-top:1.1rem; color:#666;
        font-size:0.78rem; }

    /* History expander label — green + bold */
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary {
        color:#30d158 !important;
        font-weight:700 !important;
    }
    [data-testid="stExpander"] summary svg { fill:#30d158 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Display ----------
shown = st.session_state.expr if st.session_state.expr else "0"
st.markdown(f'<div class="display">{shown}</div>', unsafe_allow_html=True)

# ---------- Keypad ----------
r1 = st.columns(4)
r1[0].button("AC", key="AC", on_click=press, args=("AC",), use_container_width=True)
r1[1].button("±", key="pm", on_click=press, args=("±",), use_container_width=True)
r1[2].button("%", key="pc", on_click=press, args=("%",), use_container_width=True)
r1[3].button("÷", key="div", type="primary", on_click=press, args=("÷",), use_container_width=True)

r2 = st.columns(4)
for i, d in enumerate(["7", "8", "9"]):
    r2[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r2[3].button("×", key="mul", type="primary", on_click=press, args=("×",), use_container_width=True)

r3 = st.columns(4)
for i, d in enumerate(["4", "5", "6"]):
    r3[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r3[3].button("−", key="sub", type="primary", on_click=press, args=("−",), use_container_width=True)

r4 = st.columns(4)
for i, d in enumerate(["1", "2", "3"]):
    r4[i].button(d, key=d, on_click=press, args=(d,), use_container_width=True)
r4[3].button("+", key="add", type="primary", on_click=press, args=("+",), use_container_width=True)

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
                st.markdown(
                    f'<div style="color:#30d158;font-weight:700;'
                    f'font-size:1.05rem;">{row["expr"]} = {row["result"]}</div>',
                    unsafe_allow_html=True,
                )
    except Exception as ex:
        st.error(f"⚠️ History error:\n\n{type(ex).__name__}: {ex}")

# ---------- Footer ----------
st.markdown('<div class="footer">Developed by AKKW</div>', unsafe_allow_html=True)
