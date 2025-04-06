import streamlit as st

# === Templates ===
template_a = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you.

And if you wanted to leave us a review, we'd really appreciate it :) -- Here's a link: www.Amazon.com/ryp"""

template_b = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your replacement is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your replacement.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""

template_c = """Thanks so much for your patience. I wanted to quickly follow up with you and let you know that your order is on its way. Your USPS tracking number will be [TRACKING]. You should receive it in a few short days. However, we are asking for your patience with the delivery of your shipment.

Of course, if you have any issues, always feel free to get back in touch with us, and we'll get right back to you."""

templates = {'A': template_a, 'B': template_b, 'C': template_c}

# === UI Setup ===
st.set_page_config(page_title="🌸 Tracking Response Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: #a14c73;'>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("Paste up to **25 tracking numbers** below. Choose response type A, B, or C. Optionally add a ticket number for your own reference.")

# === Paste-Friendly Input Section ===
st.subheader("📋 Paste Your Data")

tracking_input = st.text_area("Paste Tracking Numbers (one per line):", height=250, placeholder="1Z12345E1512345676\n1Z98765E4512345678")
ticket_input = st.text_area("Paste Ticket Numbers (optional, one per line, same order):", height=250, placeholder="TKT-001\nTKT-002")
response_type = st.selectbox("Choose Response Template:", ["A", "B", "C"])
generate = st.button("✨ Generate Responses")


if generate:
    st.markdown("---")
    st.subheader("📋 Generated Messages")

    tracking_list = [line.strip() for line in tracking_input.strip().splitlines() if line.strip()]
    ticket_list = [line.strip() for line in ticket_input.strip().splitlines()]

    if not tracking_list:
        st.warning("Please enter at least one tracking number.")
    else:
        for i, tracking in enumerate(tracking_list):
            template = templates[response_type]
            filled = template.replace("[TRACKING]", tracking)

            ticket = ticket_list[i] if i < len(ticket_list) else None
            label = f"**{i+1}. Ticket #{ticket}**" if ticket else f"**{i+1}.**"

            with st.container():
                st.markdown(label)
                st.text_area("Response", value=filled, height=200, key=f"response_{i}")
                st.markdown("Copy manually from above ⬆️")
        st.balloons()
