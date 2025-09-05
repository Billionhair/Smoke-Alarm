"""Minimal dispatcher UI."""

import streamlit as st
from agent.router import optimize_route

st.title("Dispatcher")
addresses = st.text_area("Addresses (one per line)").strip().splitlines()
if st.button("Optimize") and len(addresses) >= 2:
    res = optimize_route(addresses)
    st.write("Order:")
    for i, addr in enumerate(res.order, start=1):
        st.write(f"{i}. {addr}")
    st.write(f"Distance: {res.distance_km:.1f} km")
    st.write(f"Duration: {res.duration_min:.1f} min")
    st.write(res.url)
