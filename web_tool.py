import streamlit as st
import html

# === PAGE SETUP ===
st.set_page_config(page_title="🌸 Tracking Response Generator", layout="centered")

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
.copy-btn {
    background-color: #ffe1ec;
    color: #7a0044;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: 0.3s ease;
}
.copy-btn:hover {
    background-color: #fbb8d0;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)
st.markdown("Paste up to **30** ticket and tracking numbers. Then choose the response type for all rows below.")

# === SESSION RESET BUTTON ===
def clear_form():
    st.session_state.clear()
    st.rerun()

# === TEMPLATE BANK ===
response_templates = {
    "A": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.

And if you wanted to leave us a review, we'd really appreciate it :) -- Here's a link: www.Amazon.com/ryp""",

    "B": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.""",

    "C": """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your order is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your shipment.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""
}

# === FORM INPUT ===
col1, col2 = st.columns(2)

with col1:
    ticket_input = st.text_area("🎟 Ticket Numbers (optional)", height=300, placeholder="TKT-001\nTKT-002")
with col2:
    tracking_input = st.text_area("📦 Tracking Numbers (required)", height=300, placeholder="1Z123...\n1Z456...")

default_type = st.selectbox("Response Type", ["A", "B", "C"])

# === GENERATE RESPONSES ===
if st.button("✨ Generate Responses"):
    tickets = [t.strip() for t in ticket_input.strip().split("\n") if t.strip()]
    trackings = [t.strip() for t in tracking_input.strip().split("\n") if t.strip()]
    num = min(30, len(trackings))

    if not num:
        st.warning("Please enter at least one tracking number.")
    else:
        st.markdown("## 📬 Generated Messages")

        for i in range(num):
            ticket = tickets[i] if i < len(tickets) else ""
            tracking = trackings[i]
            template = response_templates.get(default_type, response_templates["A"])
            msg = template.replace("[TRACKING]", tracking)

            st.markdown(f"### {i+1}. Ticket `{ticket}`" if ticket else f"### {i+1}.")
            st.text_area(f"Response {i+1}", msg, height=160, key=f"msg_{i}")
            st.markdown("---")

        st.button("🔄 Start Over", on_click=clear_form)
