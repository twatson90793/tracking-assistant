import streamlit as st

st.set_page_config(page_title="🌸 Tracking Response Generator", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #fff5f7;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #b14575;
        }
        .stTextArea textarea {
            font-size: 16px;
        }
        .stButton>button {
            background-color: #ffc0cb;
            color: black;
            border-radius: 8px;
            padding: 0.4em 1em;
            border: 1px solid #ff69b4;
        }
        .stButton>button:hover {
            background-color: #ffb6c1;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)
st.write("Paste up to **30 ticket and tracking numbers**, then choose the response type for each row below:")

# Templates
templates = {
    "A": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.

And if you wanted to leave us a review, we'd really appreciate it :) -- Here's a link: www.Amazon.com/ryp""",
    "B": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.""",
    "C": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your order is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your shipment.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""
}

# Input form
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        tickets_raw = st.text_area("🎟 Ticket Numbers (optional)", height=300)
    with col2:
        trackings_raw = st.text_area("📦 Tracking Numbers (required)", height=300)

    submitted = st.form_submit_button("✨ Generate Responses")

# Output
if submitted:
    tickets = [line.strip() for line in tickets_raw.strip().splitlines()]
    trackings = [line.strip() for line in trackings_raw.strip().splitlines()]
    max_rows = min(30, max(len(trackings), len(tickets)))

    # Pad shorter list
    tickets += [""] * (max_rows - len(tickets))
    trackings += [""] * (max_rows - len(trackings))

    response_types = []
    st.markdown("#### 🅰️ Select Response Type Per Line")
    for i in range(max_rows):
        col1, col2, col3 = st.columns([2, 4, 2])
        col1.text_input("Ticket", value=tickets[i], disabled=True, key=f"ticket_disp_{i}")
        col2.text_input("Tracking", value=trackings[i], disabled=True, key=f"track_disp_{i}")
        choice = col3.selectbox("Type", ["A", "B", "C"], key=f"resp_choice_{i}")
        response_types.append(choice)

    st.markdown("---")
    st.markdown("### 📬 Your Generated Messages")

    for i in range(max_rows):
        ticket = tickets[i]
        tracking = trackings[i]
        choice = response_types[i]
        if not tracking:
            continue
        message = templates[choice].replace("[TRACKING]", tracking)
        label = f"**{i+1}. Ticket #{ticket}**" if ticket else f"**{i+1}.**"
        st.markdown(label)
        st.text_area("Response", value=message, height=160, key=f"msg_{i}")

    # Start Over button
    st.markdown("---")
    if st.button("🔁 Start Over"):
        st.rerun()
