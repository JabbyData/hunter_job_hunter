"""
Module to scrape websites
"""

from jobspy import scrape_jobs
import streamlit as st


def find_jobs(search_criteria):

    with st.spinner("Finding jobs ..."):
        jobs = scrape_jobs(
            site_name=[
                "linkedin",
            ],
            search_term=search_criteria["job_title"],
            location=search_criteria["city"] + "," + search_criteria["country"],
            job_type=search_criteria["job_type"].lower(),
            results_wanted=10,  # for each site
            hours_old=180,
            country_indeed=search_criteria["country"],
            linkedin_fetch_description=True,
        )
    st.markdown(
        f"<h3 style='text-align: center;'>Found {len(jobs)} jobs !</h3>",
        unsafe_allow_html=True,
    )
    return jobs
