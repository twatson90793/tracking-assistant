import streamlit as st
import html

st.set_page_config(page_title="🌸 Tracking Response Generator", layout="wide")

# 🌸 Pretty Styling
st.markdown("""
<style>
body {
    background-color: #fff5f7;
}
h1 {
    text-align: center;
    color: #b14575;
    font-size: 2.5em;
    margin-bottom: 10px;
}
.button-copy {
    background-color: #ffe1ec;
    color: #7a0044;
    border: none;
    padding: 8px 16px;
    border-radius: 10px;
    font-size: 14px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: 0.3s ease;
}
.button-copy:hover {
    background-color: #fbb8d0;
    color: black;
}
.copied-toast {
    display: inline-block;
    margin-left: 10px;
    font-size: 14px;
    color: green;
    animation: fadeOut 2s forwards;
}
@keyframes fadeOut {
    0% {opacity: 1;}
    100% {opacity: 0;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌸 Tracking Response Generator 🌸</h1>", unsafe_allow_html=True)

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

# Form inputs
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        tickets_raw = st.text_area("🎟 Ticket Numbers (optional)", height=300)
    with col2:
        trackings_raw = st.text_area("📦 Tracking Numbers (required)", height=300)

    submitted = st.form_submit_button("✨ Generate Responses")

# Process inputs
if submitted:
    tickets = [line.strip() for line in tickets_raw.strip().splitlines()]
    trackings = [line.strip() for line in trackings_raw.strip().splitlines()]
    max_rows = min(30, max(len(trackings), len(tickets)))

    # Pad shorter list
    tickets += [""] * (max_rows - len(tickets))
    trackings += [""] * (max_rows - len(trackings))

    # Dropdowns
    st.markdown("#### 🅰️ Select Response Type Per Line")
    response_types = []
    for i in range(max_rows):
        col1, col2, col3 = st.columns([2, 4, 2])
        col1.text_input("Ticket", value=tickets[i], disabled=True, key=f"ticket_disp_{i}")
        col2.text_input("Tracking", value=trackings[i], disabled=True, key=f"track_disp_{i}")
        choice = col3.selectbox("Type", ["A", "B", "C"], key=f"resp_choice_{i}")
        response_types.append(choice)

    # Generate messages
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
        st.text_area("Response", value=message, height=160, key=f"ta_{i}")

        # JS-based copy workaround
        safe_msg = html.escape(message).replace('\n', '\\n').replace("`", "\\`")
        st.markdown(f"""
            <div>
                <button class="button-copy" onclick="copyText_{i}()">📋 Copy Response {i+1}</button>
                <span id="toast-{i}" class="copied-toast" style="display:none;">Copied!</span>
            </div>
            <script>
            function copyText_{i}() {{
                navigator.clipboard.writeText(`{safe_msg}`);
                var toast = document.getElementById("toast-{i}");
                toast.style.display = "inline-block";
                setTimeout(() => {{
                    toast.style.display = "none";
                }}, 2000);
            }}
            </script>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔁 Start Over"):
        st.rerun()
