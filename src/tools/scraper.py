"""
Module to scrape websites
"""

import csv
import os
from jobspy import scrape_jobs
import streamlit as st


def find_jobs(search_criteria):
    print("Scraping jobs ...")

    with st.spinner("Finding jobs ..."):
        jobs = scrape_jobs(
            site_name=[
                "indeed",
                "linkedin",
            ],
            search_term=search_criteria["job_title"],
            location=search_criteria["city"] + "," + search_criteria["country"],
            job_type=search_criteria["job_type"].lower(),
            results_wanted=50,  # for each site
            hours_old=180,
            country_indeed=search_criteria["country"],
        )
    st.markdown(
        f"<h3 style='text-align: center;'>Found {len(jobs)} jobs !</h3>",
        unsafe_allow_html=True,
    )
    print(f"Found {len(jobs)} jobs !")
    return jobs
