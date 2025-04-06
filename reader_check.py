import streamlit as st
import pandas as pd
from io import BytesIO

# Hardcoded supervisor name for "security"
SUPERVISOR_NAME = "George N"

def authenticate_user():
    st.title("🔒 Secure Access Portal")
    passcode = st.text_input("Enter Supervisor Name to Continue", type="password")

    if passcode != SUPERVISOR_NAME:
        st.error("⚠️ UNAUTHORIZED ACCESS. Your activity is being logged.")
        st.markdown("""
            <div style="border: 2px solid red; padding: 1em; background-color: #ffe6e6;">
                <strong>WARNING:</strong><br>
                Unauthorized use of this application is a federal offense.<br>
                If you are not <b>Henderson</b>, cease usage immediately.<br>
                Violators will be prosecuted to the full extent of the law.
            </div>
        """, unsafe_allow_html=True)
        st.stop()
    else:
        st.success("Access granted.")
        return True

def process_file(file, reader_ids):
    df = pd.read_excel(file)

    if "Object 1 Name" not in df.columns or "Message Text" not in df.columns:
        st.error("Excel must contain 'Object 1 Name' and 'Message Text' columns.")
        return

    officer_groups = df.groupby("Object 1 Name")

    for officer_name, group in officer_groups:
        messages = " ".join(group["Message Text"].astype(str).values)
        did_not_visit = [reader for reader in reader_ids if reader not in messages]

        st.markdown(f"### 👮 Officer: `{officer_name}`")
        if did_not_visit:
            st.error(f"❌ Readers NOT Visited: {', '.join(did_not_visit)}")
        else:
            st.success("✅ All readers accounted for.")

def main():
    if authenticate_user():
        st.header("📊 Reader Audit Tool")

        uploaded_file = st.file_uploader("Upload your .xlsx file", type=["xlsx"])
        reader_input = st.text_input("Enter reader IDs (comma-separated)", placeholder="e.g., R017,R112,R999")

        if uploaded_file and reader_input:
            reader_ids = [r.strip() for r in reader_input.split(",") if r.strip()]
            process_file(uploaded_file, reader_ids)

# Run the app
if __name__ == "__main__":
    main()
