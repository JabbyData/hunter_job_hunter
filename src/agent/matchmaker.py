"""
Module to implement a matchmaker agent
"""

import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import subprocess
import time
import streamlit as st


def extract_job_info(job_description: str, llm: OllamaLLM):
    job_prompt = PromptTemplate.from_template(
        """You are an expert analyst.

        TASK: Extract the following entries from the JOB DESCRIPTION:
            0. Job title.
            1. Industry,  business area the job is dealing with.
            2. City location. Make sure to output a valid city name.
            3. Country location. Make sure to output a valid country name.
            4. Job type : should be converted into one of the following values ["fulltime", "parttime", "internship", "contract].
            5. Job level : should be converted into one of the following values ["internship", "entry-level", "mid-senior level", "executive"].
            6. Minimum salary.
            7. Maximum salary.
            8. List of education requirements. For each education requirement :
                a) Add the couple (degree level, area of study) in the EDUCATION LIST. Degree level should be one of the following values ["BSc","MSc","PhD"].
            9. List of experience requirements. For each experience requirement :
                a) Add the couple (area, duration) to the EXPERIENCE LIST. Duration should be in months.
            10. List of skills requirements, For each skill requirement:
                a) Add the couple (skill, proficiency) to the SKILL LIST. Proficiency should be one of the following values ["beginner", "intermediate", "expert"].
            
        IMPORTANT RULES:
            1. If value are missing, replace them with -1.
            2. Respect the output format. Do not use extra explanation.
        
        OUTPUT FORMAT:
            {{"job_title": job title,"industry": industry,"city": city,"country": country"job_type": job type,"seniority": entry level,"min_salary": min salary,"max_salary": max salary,"education": EDUCATION LIST,"experience": EXPERIENCE LIST,"skills": SKILL LIST}}
            
        JOB DESCRIPTION:
        {job_description}
                
        OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = job_prompt | llm | out_parser

    structured_job_info = chain.invoke({"job_description": job_description})

    start_idx = structured_job_info.find("{")
    end_idx = structured_job_info.find("}")

    return structured_job_info[start_idx : end_idx + 1]


def match_job_profile(
    user_profile: dict,
    search_criteria: dict,
    structured_job_info: dict,
    llm: OllamaLLM,
):
    match_prompt = PromptTemplate.from_template(
        """
        You are a professional recruiter.

        Task : Compare entries from USER_PROFILE and its SEARCH_CRITERIA with the requirements of STRUCTURED_JOB_INFO and decide if the candidate is a good match for the job.

        IMPORTANT RULES:
            1. USER_PROFILE, SEARCH_CRITERIA and STRUCTURED_JOB_INFO are presented as dictionnaries. Use key / value pairs to match requirements with user's profile and search.
            2. "-1" or -1 values are not comparable, skip them.
            3. If cities from SEARCH_CRITERIA AND STRUCTURED_JOB_INFO are not the same, compare distance.
            3. Output a boolean MATCH_BOOL indicating if the user is a good candidate for the job. Output a short MATCH_DESCRIPTION (less than 100 words) arguing why the candidate is or isn't a good match.
            4. Output only the couple (MATCH_BOOL,MATCH_DESCRIPTION). No extra explanation.

        USER PROFILE:
        {user_profile}

        SEARCH CRITERIA:
        {search_criteria}

        STRUCTURED_JOB_INFO:
        {structured_job_info}

        OUTPUT FORMAT: 
        (MATCH_BOOL,MATCH_DESCRIPTION)
        """
    )

    out_parser = StrOutputParser()

    match_chain = match_prompt | llm | out_parser
    match_output = match_chain.invoke(
        {
            "user_profile": user_profile,
            "search_criteria": search_criteria,
            "structured_job_info": structured_job_info,
        }
    )

    return match_output


def filter_jobs(user_profile: dict, search_criteria: dict, jobs: pd.DataFrame) -> float:
    try:
        subprocess.Popen(
            ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(2)
    except Exception as e:
        print(f"Failed to start Ollama server: {e}")

    llm = OllamaLLM(model="gemma3:27b")

    idx_job, agent_message = [], []
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_jobs = len(jobs["description"])

    for i, job_description in enumerate(jobs["description"]):
        progress = (i + 1) / total_jobs
        progress_bar.progress(progress)
        status_text.text(f"Analyzing job {i + 1}/{total_jobs}...")

        structured_job_info = extract_job_info(job_description, llm)

        match_output = (
            match_job_profile(user_profile, search_criteria, structured_job_info, llm)
            .strip("()")
            .split(", ")
        )
        if match_output[0].lower() == "true":
            idx_job.append(i)
            agent_message.append(", ".join(match_output[1:]).replace(")", ""))

    progress_bar.empty()
    status_text.empty()
    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False)
        time.sleep(2)
    except Exception as e:
        print(f"Failed to kill Ollama server: {e}")

    return idx_job, agent_message
