import streamlit as st
import pandas as pd
from datetime import datetime
from db import init_db, save_case, save_unknown, save_reference, get_cases, get_unknowns, get_references
from genetics import validate_profile, compare_profiles, MARKERS

st.set_page_config(page_title="GEN-ID", page_icon="🧬", layout="wide")
init_db()

st.title("🧬 GEN-ID")
st.caption("Computational Forensic Genetic Identification — educational prototype")
st.warning("EDUCATIONAL PROTOTYPE: uses synthetic profiles only. Not validated for real forensic casework.")

page = st.sidebar.radio("Navigation", ["Dashboard","Create Case","Unknown Samples","Family References","Matching Engine","Expert Review","Reports"])

if page == "Dashboard":
    cases, unknowns, refs = get_cases(), get_unknowns(), get_references()
    a,b,c,d = st.columns(4)
    a.metric("Cases", len(cases)); b.metric("Unknown Profiles", len(unknowns))
    c.metric("Reference Samples", len(refs)); d.metric("Data", "Synthetic")
    st.subheader("Workflow")
    st.write("Case → unknown profile → family references → computational comparison → candidate ranking → expert review → report")
    st.info("The computer accelerates comparison and organization; a qualified expert remains responsible for interpretation.")

elif page == "Create Case":
    st.header("Create Case")
    with st.form("case"):
        cid = st.text_input("Case ID", f"CASE-{datetime.now():%Y%m%d-%H%M%S}")
        incident = st.text_input("Incident", "Synthetic Mass-Casualty Demonstration")
        date = st.date_input("Incident date")
        location = st.text_input("Location", "Synthetic / Demonstration")
        if st.form_submit_button("Create Case"):
            save_case(cid, incident, str(date), location); st.success(f"Created {cid}")

elif page in ["Unknown Samples","Family References"]:
    cases = get_cases()
    if not cases:
        st.info("Create a case first.")
    else:
        is_unknown = page == "Unknown Samples"
        st.header("Register Unknown DNA Profile" if is_unknown else "Register Family Reference")
        case_id = st.selectbox("Case", [x[0] for x in cases])
        if is_unknown:
            sample_id = st.text_input("Unknown sample ID", "PM-001")
            quality = st.select_slider("Profile quality", ["Poor","Partial","Good"], value="Good")
        else:
            family_id = st.text_input("Family ID", "FAM-001")
            ref_id = st.text_input("Reference sample ID", "REF-001")
            relationship = st.selectbox("Relationship", ["Parent","Sibling","Child","Other relative"])
        st.subheader("Synthetic STR-style profile")
        data = {}
        cols = st.columns(4)
        for i, marker in enumerate(MARKERS):
            with cols[i % 4]:
                x = st.text_input(f"{marker} allele 1", key=f"{'u' if is_unknown else 'r'}1_{marker}")
                y = st.text_input(f"{marker} allele 2", key=f"{'u' if is_unknown else 'r'}2_{marker}")
                data[marker] = (x,y)
        if st.button("Save Profile"):
            ok,msg = validate_profile(data)
            if not ok: st.error(msg)
            elif is_unknown:
                save_unknown(case_id, sample_id, quality, data); st.success("Unknown synthetic profile saved.")
            else:
                save_reference(case_id, family_id, ref_id, relationship, data); st.success("Reference synthetic profile saved.")

elif page == "Matching Engine":
    st.header("Computational Candidate Ranking")
    unknowns, refs = get_unknowns(), get_references()
    if not unknowns or not refs:
        st.info("Add at least one unknown profile and one family reference.")
    else:
        uid = st.selectbox("Unknown sample", [x[1] for x in unknowns])
        u = next(x for x in unknowns if x[1] == uid)
        rows = []
        for r in refs:
            score, matched, compared = compare_profiles(u[3], r[4])
            rows.append({"Family":r[1],"Reference":r[2],"Relationship":r[3],
                         "Compatibility score":score,"Markers compared":compared,
                         "Overlapping markers":matched})
        df = pd.DataFrame(rows).sort_values("Compatibility score", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("This score is an educational similarity metric, NOT a forensic likelihood ratio, identity probability, or legal conclusion.")
        st.bar_chart(df.set_index("Family")["Compatibility score"])

elif page == "Expert Review":
    st.header("Expert Review")
    st.write("Review profile quality, relationship assumptions, candidate ranking and supporting evidence.")
    st.selectbox("Review status", ["Pending","Needs additional testing","Supported for further verification","Not supported"])
    st.text_area("Reviewer notes")
    st.button("Save Review")
    st.info("The prototype intentionally does not make an autonomous identity decision.")

else:
    st.header("Synthetic Analysis Report")
    st.write("Presentation-ready report summary.")
    cases = get_cases()
    if cases:
        cid = st.selectbox("Case", [x[0] for x in cases])
        st.code(f"""GEN-ID — SYNTHETIC DEMONSTRATION REPORT
Case: {cid}
Generated: {datetime.now():%Y-%m-%d %H:%M}

Purpose:
Organize and computationally compare synthetic forensic DNA-style profiles.

Status:
Educational prototype — not validated for forensic use.

Workflow:
1. Register unknown profile
2. Register family references
3. Compare profiles computationally
4. Rank candidates
5. Human expert review required
""")
