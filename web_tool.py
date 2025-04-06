import streamlit as st

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
st.markdown("---")

st.subheader("📋 Paste Spreadsheet Columns")

cols = st.columns(3)
with cols[0]:
    ticket_input = st.text_area("Ticket Numbers (optional, one per line)", height=300, placeholder="TKT-001\nTKT-002")
with cols[1]:
    tracking_input = st.text_area("Tracking Numbers (required, one per line)", height=300, placeholder="1Z12345E1512345676\n1Z98765E4512345678")
with cols[2]:
    response_input = st.text_area("Response Type (A, B, or C — one per line)", height=300, placeholder="A\nB")

generate = st.button("✨ Generate Responses")

# === Response Output ===
if generate:
    st.markdown("---")
    st.subheader("📦 Generated Messages")

    # Split lines
    tickets = [line.strip() for line in ticket_input.strip().splitlines()]
    trackings = [line.strip() for line in tracking_input.strip().splitlines()]
    responses = [line.strip().upper() for line in response_input.strip().splitlines()]

    if not trackings:
        st.warning("Please enter at least one tracking number.")
    elif len(trackings) != len(responses):
        st.error("The number of tracking numbers and response types must match.")
    else:
        for i, tracking in enumerate(trackings):
            response_type = responses[i] if i < len(responses) else "A"
            ticket = tickets[i] if i < len(tickets) else None
            template = templates.get(response_type, template_a)
            filled = template.replace("[TRACKING]", tracking)

            header = f"**{i+1}. Ticket #{ticket}**" if ticket else f"**{i+1}.**"
            with st.container():
                st.markdown(header)
                st.text_area("Response", value=filled, height=200, key=f"response_{i}")
                st.markdown("Copy manually above ⬆️")
        st.balloons()
