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
st.markdown("<style>body {background-color: #fff5f7;}</style>", unsafe_allow_html=True)

st.markdown("Paste up to **30 ticket and tracking numbers**, then select the response type for each row below:")

# === Step 1: Paste columns A + B ===
cols = st.columns(2)
with cols[0]:
    tickets_raw = st.text_area("🎟 Ticket Numbers (optional)", height=400, placeholder="TKT-001\nTKT-002\n...")
with cols[1]:
    trackings_raw = st.text_area("📦 Tracking Numbers (required)", height=400, placeholder="1Z123...\n1Z456...\n...")

# === Step 2: Process pasted data ===
tickets = [line.strip() for line in tickets_raw.strip().splitlines()]
trackings = [line.strip() for line in trackings_raw.strip().splitlines()]
num_rows = min(30, len(trackings))

if num_rows:
    st.markdown("---")
    st.subheader("🅰️ Select Response Type Per Row")

    response_types = []
    for i in range(num_rows):
        row = st.columns([2, 4, 2])
        ticket_display = tickets[i] if i < len(tickets) else ""
        tracking_display = trackings[i]
        row[0].text_input("Ticket", value=ticket_display, disabled=True, key=f"ticket_disp_{i}")
        row[1].text_input("Tracking", value=tracking_display, disabled=True, key=f"track_disp_{i}")
        choice = row[2].selectbox("Type", ["A", "B", "C"], key=f"resp_choice_{i}")
        response_types.append(choice)

    if st.button("✨ Generate Responses"):
        st.markdown("---")
        st.subheader("📬 Your Generated Messages")

        for i in range(num_rows):
            tracking = trackings[i]
            ticket = tickets[i] if i < len(tickets) else ""
            template = templates.get(response_types[i], template_a)
            message = template.replace("[TRACKING]", tracking)

            label = f"**{i+1}. Ticket #{ticket}**" if ticket else f"**{i+1}.**"
            with st.container():
                st.markdown(label)
                st.text_area("Response", value=message, height=200, key=f"response_out_{i}")
                st.markdown("Copy manually from above ⬆️")

        st.success("Responses generated! 🌸")
        st.balloons()
else:
    st.info("Paste at least one tracking number to continue.")
