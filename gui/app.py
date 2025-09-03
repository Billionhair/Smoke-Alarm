import sys
from pathlib import Path

# Ensure agent package is importable when running from repo root
sys.path.append(str(Path(__file__).resolve().parents[1] / 'agent' / 'src'))

import pandas as pd
import streamlit as st
from datetime import date

from agent.sheets import SheetDB
from agent.router import build_route_url

st.set_page_config(page_title="Smoke Alarm Agent")
st.title("Smoke Alarm Agent GUI")

route_tab, leads_tab = st.tabs(["Route Planner", "Leads Enrichment"])

with route_tab:
    st.header("Route Planner")
    d = st.date_input("Inspection date", value=date.today())
    if st.button("Build Route"):
        db = SheetDB()
        props = db.list_properties_due(d.isoformat())
        addrs = [db.format_address(p) for p in props]
        if addrs:
            url = build_route_url(addrs)
            st.success("Route URL:")
            st.write(url)
        else:
            st.info(f"No properties due for {d.isoformat()}")

with leads_tab:
    st.header("Leads Enrichment")
    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        df.columns = [c.strip().title() for c in df.columns]
        keep = ["Name", "Phone", "Email", "Website", "Suburb"]
        for k in keep:
            if k not in df.columns:
                df[k] = ""
        df = df[keep].drop_duplicates().reset_index(drop=True)
        st.download_button(
            "Download enriched CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="leads_enriched.csv",
            mime="text/csv",
        )
