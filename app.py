import streamlit as st
import os
import json

# ---- Access Codes ----
ADMIN_PASS = "admin123"
VOTER_PASS = "vote123"
DATA_FILE = "votes.json"
# ---- Functions ----
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"position": None, "candidates": [], "votes": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---- Initial Load ----
data = load_data()

# ---- Session State ----
if "role" not in st.session_state:
    st.session_state.role = None
if "voted" not in st.session_state:
    st.session_state.voted = False

# ---- UI ----
st.title("🗳️ Toastmasters Voting App")

# ---- Access Code ----
if st.session_state.role is None:
    code = st.text_input("Enter access code:", type="password")
    if code == ADMIN_PASS:
        st.session_state.role = "admin"
    elif code == VOTER_PASS:
        st.session_state.role = "voter"
    elif code:
        st.error("Invalid code. Try again.")

# ---- Admin Panel ----
if st.session_state.role == "admin":
    st.subheader("🔧 Admin Panel")
    position = st.text_input("Enter position/title (e.g. Best Speaker):", value=data.get("position") or "")
    candidate_input = st.text_area("Enter participant names (one per line):")

    if st.button("Start / Update Voting"):
        candidates = [name.strip() for name in candidate_input.split("\n") if name.strip()]
        votes = {name: 0 for name in candidates}
        data = {"position": position, "candidates": candidates, "votes": votes}
        save_data(data)
        st.success("Voting session updated!")

    # Load updated data
    data = load_data()
    if data["candidates"]:
        st.markdown("---")
        st.subheader(f"📊 Live Results: {data['position']}")
        for name, count in data["votes"].items():
            st.write(f"**{name}**: {count} vote(s)")

# ---- Voter Panel ----
elif st.session_state.role == "voter":
    data = load_data()
    if not data["position"] or not data["candidates"]:
        st.warning("Voting session has not started yet. Please check back later.")
    elif st.session_state.voted:
        st.info("✅ You have already voted. Thank you!")
    else:
        st.subheader(f"🗳️ Vote for: {data['position']}")
        vote = st.radio("Select your candidate:", data["candidates"])
        if st.button("Submit Vote"):
            data["votes"][vote] += 1
            save_data(data)
            st.session_state.voted = True
            st.success("Your vote has been submitted!")

# ---- Footer ----
st.markdown("---")
st.caption("Toastmasters Voting App · Powered by Streamlit")