import streamlit as st
import pandas as pd
from src.database import init_db, get_db, LogRecord
from src.ingestion import fetch_cloud_logs
from src.llm import ErrorResolver

# Initialize App
st.set_page_config(page_title="LogOps AI", layout="wide", page_icon="🛡️")
init_db()
db = next(get_db())

if "resolver" not in st.session_state:
    st.session_state.resolver = ErrorResolver()

# Header & Actions
st.title("🛡️ LogOps AI: Real-Time Log Resolver")
st.markdown("### ⚡ Live System Monitor")

col_act1, col_act2 = st.columns([1, 5])

with col_act1:
    if st.button("📥 Poll Log Stream"):
        with st.spinner("Reading live logs..."):
            count = fetch_cloud_logs(db)
        
        if count > 0:
            st.toast(f"🚨 ALERT: {count} new Critical Errors detected!", icon="🔥")
            st.rerun()
        else:
            st.toast("System healthy. No new errors found.", icon="✅")

# Data Fetching
logs = db.query(LogRecord).order_by(LogRecord.timestamp.desc()).all()
if not logs:
    st.info("Waiting for incoming log stream... Run 'python log_emitter.py' in a separate terminal.")
    st.stop()

# Display Logs (Master View)
data = [{
    "ID": l.id, 
    "Time": l.timestamp.strftime("%H:%M:%S"), 
    "Service": l.service_name, 
    "Severity": l.severity, 
    "Status": "✅ Resolved" if l.is_resolved else "❌ Pending"
} for l in logs]

df = pd.DataFrame(data)
# Highlight rows based on severity
st.dataframe(df, use_container_width=True)

# Detail View & Resolution
st.divider()
st.subheader("🛠️ Resolution Workspace")

selected_id = st.selectbox("Select Log ID to Resolve:", options=[l.id for l in logs])
log_to_solve = db.query(LogRecord).filter(LogRecord.id == selected_id).first()

if log_to_solve:
    c1, c2 = st.columns(2)
    with c1:
        st.error(f"**Error Message:**\n\n{log_to_solve.message}")
        st.text(f"Service: {log_to_solve.service_name}")
        
    with c2:
        if log_to_solve.is_resolved:
            st.success("Analysis Complete")
            with st.expander("See Root Cause"):
                st.write(log_to_solve.ai_root_cause)
            with st.expander("Suggested Fix Steps"):
                st.write(log_to_solve.ai_suggested_fix)
            st.code(log_to_solve.ai_generated_code, language="bash")
        
        else:
            if st.button(f"⚡ Auto-Resolve Log #{selected_id}"):
                with st.spinner("Consulting Knowledge Base & Generating Fix..."):
                    result = st.session_state.resolver.resolve(log_to_solve)
                    
                    log_to_solve.ai_root_cause = result['root_cause']
                    log_to_solve.ai_suggested_fix = result['fix_steps']
                    log_to_solve.ai_generated_code = result['code_snippet']
                    log_to_solve.is_resolved = True
                    db.commit()
                    st.rerun()
