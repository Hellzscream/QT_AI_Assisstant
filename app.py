import streamlit as st
import time
import json
from cve_finder import extract_cve_ids, fetch_cve_details
from embed_and_store import embed_and_store_from_entries  # NEW: import embedding function

def main():
    st.set_page_config(page_title="QT secANALYST", layout="centered")

    st.markdown("""
        <style>
            .main {
                background-color: #FFFFFF;
            }
            .block-container {
                background-color: #F0F0F0;
                padding: 3rem 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                max-width: 700px;
                margin: 5vh auto;
                color: #000000;
            }
            h1, h2, h3, .subheading {
                text-align: center !important;
                color: #000000 !important;
            }
            .subheading {
                font-size: 1.1rem;
                margin-bottom: 2rem;
            }
            .stButton button {
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 24px;
                border-radius: 8px;
                border: none;
                font-weight: bold;
            }
            .button-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-top: 2rem;
                gap: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## Hi, I am QT secANALYST")
    st.markdown("<div class='subheading'>Please upload scan document, that our agent will read for you</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload .txt or .json file", type=["txt", "json"])

    if uploaded_file:
        # Detect file type
        file_extension = uploaded_file.name.split('.')[-1]

        try:
            if file_extension == "txt":
                text = uploaded_file.read().decode("utf-8")
            elif file_extension == "json":
                json_data = json.load(uploaded_file)
                text = json.dumps(json_data)
            else:
                st.error("Unsupported file type.")
                return
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        message_placeholder = st.empty()
        progress = st.progress(0)

        for percent in range(100):
            dots = "." * ((percent // 10) % 4)
            message_placeholder.markdown(
                f"<h4 style='text-align:center; color:#444;'>AI agent is reading{dots}</h4>",
                unsafe_allow_html=True
            )
            progress.progress(percent + 1)
            time.sleep(0.03)

        cve_ids = extract_cve_ids(text)
        api_key = ""

        cve_data = []
        for cve_id in cve_ids:
            description, links = fetch_cve_details(cve_id, api_key)
            cve_data.append((cve_id, description, links))

        # Write to file and prepare entries for embedding
        cve_entries = []
        with open("extracted_cves.txt", "w") as f:
            for cve_id, description, links in cve_data:
                entry = f"CVE ID: {cve_id}\nDescription: {description}\n"
                if links:
                    entry += "Links:\n" + "\n".join([f"  - {link}" for link in links])
                entry += "\n" + "-" * 85 + "\n"
                f.write(entry)
                cve_entries.append(entry)

        embed_and_store_from_entries(cve_entries)

        st.markdown(f"""
            <div style="background-color:#d4edda; padding:1rem; border-radius:8px; border:1px solid #c3e6cb; color:#000000; text-align:center;">
                Extracted and stored {len(cve_data)} CVE IDs with descriptions and links.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="button-container">', unsafe_allow_html=True)

        with open("extracted_cves.txt", "rb") as file:
            st.download_button(
                label="⬇️ Download Extracted CVEs",
                data=file,
                file_name="extracted_cves.txt",
                mime="text/plain",
                key="download_button"
            )

        if st.button("Confirm and Proceed to Chat 💬", key="confirm_button"):
            message_placeholder.markdown(
                "<h4 style='text-align:center; color:#444;'>🚶 Moving to conference room...</h4>",
                unsafe_allow_html=True
            )
            time.sleep(2)
            st.switch_page("pages/1_Chat.py")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
