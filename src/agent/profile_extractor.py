"""
Module containing langchain functions
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import subprocess
import time


def extract_profile_info(llm: OllamaLLM, text_resume: str):
    profile_prompt = PromptTemplate.from_template(
        """You are an expert resume parser specializing in business information extraction.

        TASK: Extract all education, experience, project and skill related entries from text_resume, with focus on business-relevant information.

        EXTRACTION RULES:
        1. Output ONLY valid DICT format.
        2. No additional text, comments, or explanations.
        3. Education results are stored in a list. For each education entry:
            a) Add the couple (degree level, area of study) to the EDUCATION LIST.
        4. Degree level should be converted to one of these values ["bsc","msc","phd"].
        5. Experience and project results are stored in a list. For each experience and project entry :
            a) Add the couple (description, duration in months) to the EXPERIENCE / PROJECT LIST.
        6. Experience and project entries should be considered as experience in the output. Make sure to treat ALL entries.
        7. Skill results are stored in a list. For each skill entry:
            a) Add the couple (skill, proficiency) to the SKILL LIST.
            b) Proficiency should be converted to one of these values : ["beginner","intermediate","expert"]. Infer from description associated with the skill.
        9. If information is missing, replace it by -1.
        10. No indentation or formatting.
        11. Use lower case style.

        OUTPUT FORMAT:
            {{"education": EDUCATION LIST,
            "experience": EXPERIENCE / PROJECT LIST,
            "skill": SKILL LIST}}

        RESUME TEXT:
        {text_resume}

        OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = profile_prompt | llm | out_parser

    profile_analysis = chain.invoke({"text_resume": text_resume})

    return profile_analysis


def analyse_profile(llm, text_resume, max_failure):
    failure_c = 0
    topic_analysis = None
    while failure_c < max_failure:

        try:
            topic_analysis = extract_profile_info(llm, text_resume)
            start_idx = topic_analysis.find("{")
            end_idx = topic_analysis.find("}")
            topic_analysis = topic_analysis[start_idx : end_idx + 1]
            break

        except Exception as e:
            failure_c += 1
            print(f"Profile extraction failed (attempt {failure_c}): {e}")

    return topic_analysis


def extract_profile(text_resume: str, max_failure: int = 10):
    try:

        try:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(2)
        except Exception as e:
            print(f"Failed to strat Ollama server: {e}")

        llm = OllamaLLM(model="gemma3:27b")

        with st.spinner(f"Extracting user profile..."):
            resume_analysis = analyse_profile(llm, text_resume, max_failure)

        st.text("Profile extracted !")

        with st.spinner(f"Recommending jobs ..."):
            st.session_state.rec_analysis = recommend_job(resume_analysis, llm)

        return resume_analysis

    except Exception as e:
        st.text("⚠️ Profile extraction failed, please try again.")
        print(e)


def recommend_job(profile_description: str, llm: OllamaLLM, max_failure: int = 10):
    failure_c = 0
    while failure_c < max_failure:
        try:
            print("Recommending job positions ...")

            rec_prompt = PromptTemplate.from_template(
                """You are a career advisor.

            TASK: Find job positions related to the profile description.

            IMPORTANT RULES:
            1. Output a list of at most 10 relevant jobs based on the profile description
            2. No additional text, comments, or explanations
            3. No identation
            4. Output ONLY the list

            OUTPUT_FORMAT:
            ["job1", "job2", ... , "job10"]

            RESUME TEXT:
            {profile_description}

            OUTPUT:"""
            )

            out_parser = StrOutputParser()

            rec_pipe = rec_prompt | llm | out_parser

            rec_analysis = rec_pipe.invoke({"profile_description": profile_description})

            return rec_analysis

        except Exception as e:
            failure_c += 1
            print(f"Education extraction failed (attempt {failure_c}): {e}")

    if failure_c == max_failure:
        st.text("⚠️ Job recommendation failed, please try again.")
