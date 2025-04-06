import streamlit as st
import pyperclip

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

with st.form("tracking_form"):
    cols = st.columns([3, 3, 1])
    tracking_numbers = []
    ticket_numbers = []
    response_choices = []

    for i in range(25):
        with cols[0]:
            tracking = st.text_input(f"Tracking #{i+1}", key=f"tracking_{i}")
        with cols[1]:
            ticket = st.text_input("Ticket # (optional)", key=f"ticket_{i}")
        with cols[2]:
            response = st.selectbox("Type", options=["A", "B", "C"], key=f"resp_{i}")

        tracking_numbers.append(tracking.strip())
        ticket_numbers.append(ticket.strip())
        response_choices.append(response)

    submitted = st.form_submit_button("✨ Generate Responses")

if submitted:
    st.markdown("---")
    st.subheader("📋 Generated Messages")

    if not any(tracking_numbers):
        st.warning("Please enter at least one tracking number.")
    else:
        for i, tracking in enumerate(tracking_numbers):
            if tracking:
                template = templates[response_choices[i]]
                filled = template.replace("[TRACKING]", tracking)
                ticket = ticket_numbers[i]

                if ticket:
                    label = f"**{i+1}. Ticket #{ticket}**"
                else:
                    label = f"**{i+1}.**"

                with st.container():
                    st.markdown(label)
                    st.text_area("Response", value=filled, height=200, key=f"response_{i}")
                    copy_button = st.button("📋 Copy to Clipboard", key=f"copy_{i}")
                    if copy_button:
                        try:
                            pyperclip.copy(filled)
                            st.success("Copied to clipboard!")
                        except Exception:
                            st.warning("Copy failed — this only works locally. On Streamlit Cloud, copy manually.")

        st.balloons()
