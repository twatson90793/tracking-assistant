import streamlit as st

def reset_form():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# === Templates ===
template_a = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.

And if you wanted to leave us a review, we'd really appreciate it :) -- Here's a link: www.Amazon.com/ryp"""

template_b = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""

template_c = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your order is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your shipment.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""

templates = {"A": template_a, "B": template_b, "C": template_c}

# === UI Setup ===
st.set_page_config(page_title="🌸 Tracking Response Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: #a14c73;'>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)
st.markdown("<style>body {background-color: #fff5f7;}</style>", unsafe_allow_html=True)

st.markdown("Paste up to **30 ticket and tracking numbers**, then select the response type for each row below:")

col1, col2 = st.columns(2)

with col1:
    if "tickets_raw" not in st.session_state:
        st.session_state["tickets_raw"] = ""
    st.text_area("🎟 Ticket Numbers (optional)", key="tickets_raw", height=250)

with col2:
    if "trackings_raw" not in st.session_state:
        st.session_state["trackings_raw"] = ""
    st.text_area("📦 Tracking Numbers (required)", key="trackings_raw", height=250)

tickets = [line.strip() for line in st.session_state["tickets_raw"].strip().splitlines()]
trackings = [line.strip() for line in st.session_state["trackings_raw"].strip().splitlines()]
num_rows = min(30, len(trackings))

if num_rows:
    st.markdown("---")
    st.subheader("🅰️ Select Response Type Per Row")

    response_types = []
for i in range(num_rows):
    tracking = trackings[i]
    ticket = tickets[i] if i < len(tickets) else ""
    response_type = st.selectbox(
        f"Choose response type for row {i+1}",
        options=list(templates.keys()),
        index=0,
        key=f"resp_type_{i}"
    )
    response_types.append(response_type)
    template = templates.get(response_type, template_a)
    message = template.replace("[TRACKING]", tracking)

    label = f"**{i+1}. Ticket #{ticket}**" if ticket else f"**{i+1}.**"
    with st.container():
        st.markdown(label)
        st.text_area("Response", value=message, height=200, key=f"response_out_{i}")

        # Escape content for JavaScript
        escaped = message.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n").replace('"', '\\"')

        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <button onclick="copyToClipboard_{i}()" style="
                background-color:#ffe4ec;
                color:#880e4f;
                font-weight:bold;
                border:2px solid #f8bbd0;
                border-radius:10px;
                padding:6px 12px;
                font-size:14px;
                cursor:pointer;
            ">📋 Copy</button>
            <span id="copied-msg-{i}" style="display:none; margin-left:10px; color:green;">Copied!</span>
        </div>

        <script>
            function copyToClipboard_{i}() {{
                navigator.clipboard.writeText("{escaped}");
                document.getElementById("copied-msg-{i}").style.display = "inline";
                setTimeout(function() {{
                    document.getElementById("copied-msg-{i}").style.display = "none";
                }}, 2000);
            }}
        </script>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <button onclick="copyToClipboard_{i}()" style="
                background-color:#ffe4ec;
                color:#880e4f;
                font-weight:bold;
                border:2px solid #f8bbd0;
                border-radius:10px;
                padding:6px 12px;
                font-size:14px;
                cursor:pointer;
            ">📋 Copy</button>
            <span id="copied-msg-{i}" style="display:none; margin-left:10px; color:green;">Copied!</span>
        </div>

        <script>
            function copyToClipboard_{i}() {{
                navigator.clipboard.writeText("{escaped}");
                document.getElementById("copied-msg-{i}").style.display = "inline";
                setTimeout(function() {{
                    document.getElementById("copied-msg-{i}").style.display = "none";
                }}, 2000);
            }}
        </script>
        """, unsafe_allow_html=True)
                
else:
    st.info("Paste at least one tracking number to continue.")

st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ffe4ec;
        color: #880e4f;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        border: 2px solid #f8bbd0;
        transition: 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #f8bbd0;
        color: #6a1b4d;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

def reset_form():
    st.session_state.clear()
    st.rerun()

if st.button("🌸 Start Over"):
    reset_form()
