import streamlit as st

st.set_page_config(page_title="Tracking Response Generator", layout="wide")

st.markdown(
    """
    <style>
        body {
            background-color: #fff0f5;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
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
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)
st.write("Paste up to **30 ticket and tracking numbers**, then choose the response type for each row below:")

with st.form("tracking_form"):
    col1, col2 = st.columns(2)

    with col1:
        ticket_input = st.text_area("🎟️ Ticket Numbers (optional)", height=300, placeholder="TKT-001\nTKT-002\n...")

    with col2:
        tracking_input = st.text_area("📦 Tracking Numbers (required)", height=300, placeholder="1Z123...\n1Z456...\n...")

    submitted = st.form_submit_button("✨ Generate Responses")

# Canned responses
response_templates = {
    "A": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.

And if you wanted to leave us a review, we'd really appreciate it :) -- Here's a link: www.Amazon.com/ryp""",
    "B": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.""",
    "C": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your order is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your shipment.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""
}

if submitted:
    st.divider()
    st.markdown("### 📬 Your Generated Messages")
    tickets = ticket_input.strip().splitlines()
    trackings = tracking_input.strip().splitlines()

    max_len = max(len(tickets), len(trackings))
    tickets += [""] * (max_len - len(tickets))
    trackings += [""] * (max_len - len(trackings))

    response_types = []
    st.markdown("#### Select Response Type for Each Line")
    for i in range(max_len):
        response_types.append(
            st.selectbox(f"Response type for line {i+1}:", ["A", "B", "C"], key=f"dropdown_{i}")
        )

    if len(trackings) > 30:
        st.error("🚫 Please limit to 30 entries or fewer.")
    else:
        for i in range(max_len):
            ticket = tickets[i].strip()
            tracking = trackings[i].strip()
            response_type = response_types[i]

            if not tracking:
                continue

            message = response_templates[response_type].replace("[TRACKING]", tracking)

            st.markdown(f"**{i+1}. Ticket #{ticket or '(no ticket number)'}**")
            st.text_area("Response", value=message, height=150, key=f"msg_{i}")

        st.divider()
        if st.button("🔁 Start Over"):
            st.experimental_rerun()
