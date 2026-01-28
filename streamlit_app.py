# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# LLM Wrapper

def call_llm(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a multi-disciplinary COO assistant for private equity and venture capital firms."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Core Modules

def fund_admin_summary(df: pd.DataFrame) -> str:
    prompt = f"Generate a fund administration report from: {df.head(3).to_dict()}"
    return call_llm(prompt)

def investor_relations_qa(question: str, context: str) -> str:
    prompt = f"Investor question: {question}\nContext: {context}\nRespond as a professional investor relations manager."
    return call_llm(prompt)

def legal_docs_drafter(doc_type: str, details: str) -> str:
    prompt = f"Draft a {doc_type} based on this description: {details}"
    return call_llm(prompt)

def compliance_checker(text: str) -> str:
    prompt = f"Check this fund text for compliance, regulatory flags, or ESG gaps: {text}"
    return call_llm(prompt)

def treasury_optimizer(df: pd.DataFrame) -> str:
    prompt = f"Suggest treasury and cash optimization strategies based on fund flows: {df.head(3).to_dict()}"
    return call_llm(prompt)

# Streamlit UI

def main():
    st.set_page_config("Monarch AI – AI COO for Funds", page_icon="👑", layout="wide")
    st.title("👑 Monarch AI – The Autonomous Fund COO")
    st.write("Streamline ops, legal, IR, compliance, and treasury with one AI platform.")

    uploaded_file = st.file_uploader("Upload fund ops data (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
    else:
        df = pd.DataFrame()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Fund Admin",
        "👥 Investor Relations",
        "📄 Legal Drafting",
        "🛡 Compliance Check",
        "💰 Treasury & FX"
    ])

    with tab1:
        st.subheader("📋 Fund Admin Dashboard")
        if st.button("Generate Admin Summary"):
            if df.empty:
                st.error("Upload fund data.")
            else:
                admin = fund_admin_summary(df)
                st.text_area("Fund Admin Report", value=admin, height=400)

    with tab2:
        st.subheader("👥 Answer Investor Questions")
        context = st.text_area("Context (fund terms, past comms, etc.)")
        q = st.text_input("Investor Question")
        if st.button("Respond as IR"):
            if not q or not context:
                st.error("Fill both fields.")
            else:
                resp = investor_relations_qa(q, context)
                st.text_area("IR Answer", value=resp, height=300)

    with tab3:
        st.subheader("📄 Draft Legal Documents")
        doc_type = st.selectbox("Select Doc Type", ["NDA", "LPA Outline", "Term Sheet", "Deal Memo"])
        details = st.text_area("Describe What You Need")
        if st.button("Draft Document"):
            if not details:
                st.error("Provide a description.")
            else:
                doc = legal_docs_drafter(doc_type, details)
                st.text_area("Generated Document", value=doc, height=400)

    with tab4:
        st.subheader("🛡 Compliance & ESG Scan")
        text = st.text_area("Paste legal/marketing text")
        if st.button("Run Compliance Review"):
            if not text:
                st.error("Paste text to review.")
            else:
                check = compliance_checker(text)
                st.text_area("Compliance Feedback", value=check, height=400)

    with tab5:
        st.subheader("💰 Treasury Strategy Generator")
        if st.button("Suggest Treasury Moves"):
            if df.empty:
                st.error("Upload fund flow data.")
            else:
                advice = treasury_optimizer(df)
                st.text_area("Treasury Advice", value=advice, height=300)

if __name__ == "__main__":
    main()
