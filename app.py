import requests
import streamlit as st
from typing import List

# Function to run a PubMed search and get PMIDs
def get_pubmed_pmids(search_query: str, max_results: int = 1000) -> List[str]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": search_query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['esearchresult']['idlist']

# Function to compare PMIDs
def compare_pmids(retrieved_pmids: List[str], known_pmids: List[str]) -> dict:
    retrieved_set = set(retrieved_pmids)
    known_set = set(known_pmids)

    found = list(known_set & retrieved_set)
    missed = list(known_set - retrieved_set)

    return {
        "found_pmids": found,
        "missed_pmids": missed,
        "total_known": len(known_pmids),
        "found_count": len(found),
        "missed_count": len(missed)
    }

# Streamlit interface
st.title("PubMed Search String Checker")

search_query = st.text_input("Enter your PubMed Search Query:")
known_pmids_input = st.text_area("Enter known PMIDs (comma-separated):")

if st.button("Check Search String"):
    if not search_query or not known_pmids_input:
        st.warning("Please provide both a search query and known PMIDs.")
    else:
        known_pmids = [pmid.strip() for pmid in known_pmids_input.split(",") if pmid.strip()]
        try:
            retrieved_pmids = get_pubmed_pmids(search_query)
            comparison = compare_pmids(retrieved_pmids, known_pmids)

            st.write(f"### Results for Search Query:\n`{search_query}`")
            st.write(f"**Total Known PMIDs:** {comparison['total_known']}")
            st.write(f"**Found:** {comparison['found_count']} / **Missed:** {comparison['missed_count']}")

            st.write("**Found PMIDs:**")
            st.write(", ".join(comparison['found_pmids']))

            st.write("**Missed PMIDs:**")
            st.write(", ".join(comparison['missed_pmids']))

        except Exception as e:
            st.error(f"An error occurred: {e}")
