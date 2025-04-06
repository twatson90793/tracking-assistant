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

st.markdown("Paste or enter ticket numbers, tracking numbers, and select a response template for each line below.")

# === Input Table ===
data = []
st.markdown("#### ✏️ Input Rows (up to 75)")
header_cols = st.columns([2, 4, 2])
header_cols[0].markdown("**Ticket Number**")
header_cols[1].markdown("**Tracking Number**")
header_cols[2].markdown("**Response Type**")

for i in range(75):
    row = st.columns([2, 4, 2])
    ticket = row[0].text_input("Ticket", key=f"ticket_{i}")
    tracking = row[1].text_input("Tracking", key=f"tracking_{i}")
    response = row[2].selectbox("Type", options=["A", "B", "C"], index=0, key=f"response_{i}")
    data.append((ticket.strip(), tracking.strip(), response.strip()))

# === Generate Button ===
if st.button("✨ Generate Responses"):
    st.markdown("---")
    st.subheader("📦 Generated Messages")

    count = 0
    for i, (ticket, tracking, response_type) in enumerate(data):
        if tracking:
            count += 1
            template = templates.get(response_type.upper(), template_a)
            filled = template.replace("[TRACKING]", tracking)
            label = f"**{count}. Ticket #{ticket}**" if ticket else f"**{count}.**"

            with st.container():
                st.markdown(label)
                st.text_area("Response", value=filled, height=200, key=f"response_out_{i}")
                st.markdown("Copy manually from above ⬆️")

    if count == 0:
        st.warning("Please enter at least one tracking number.")
    else:
        st.balloons()
