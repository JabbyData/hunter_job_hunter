"""
Module containing langchain functions
"""

from huggingface_hub import login
from langchain_huggingface.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import streamlit as st


def extract_education(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting education ...")
    educ_prompt = PromptTemplate.from_template(
        """You are an expert resume parser.

        TASK: Extract ALL education entries from the resume.

        For each education entry, extract:
        - Institution name
        - Degree level
        - Field of study
        - Start date (format: YYYY-MM)
        - End date (format: YYYY-MM or "Present" if current)
        - Location (City, Country)

        IMPORTANT RULES:
        1. Output ONLY valid JSON format
        2. No additional text, comments, or explanations
        3. Use exact field names as shown in the format
        4. If information is missing, use empty string ""
        5. No indentation or formatting

        OUTPUT FORMAT:
        {{"education": [{{"institution": "University name", "degree_level": "Degree type", "field_of_study": "Major/Field", "start_date": "YYYY-MM", "end_date": "YYYY-MM or Present", "location": "City, Country"}}]}}

        RESUME TEXT:
        {text_resume}

        JSON OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = educ_prompt | llm | out_parser

    edu_analysis = chain.invoke({"text_resume": text_resume})

    return edu_analysis


def extract_experience(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting experience ...")
    exp_prompt = PromptTemplate.from_template(
        """You are an expert resume parser.

        TASK: Extract ALL professional work experience entries from the resume.

        For each work experience entry, extract:
        - Company name
        - Job title/position
        - Description: EXACTLY 5 keywords describing key responsibilities and technologies
        - Start date (format: YYYY-MM)
        - End date (format: YYYY-MM or "Present" if current)
        - Location (City, Country)

        IMPORTANT RULES:
        1. Output ONLY valid JSON format
        2. No additional text, comments, or explanations
        3. Use exact field names as shown in the format
        4. Description must contain MAXIMUM 5 keywords separated by commas
        5. Keywords should focus on: technologies, tools, responsibilities, achievements
        6. If information is missing, use empty string ""
        7. No indentation or formatting

        JSON FORMAT:
        {{"experience": [{{"company": "Company name", "position": "Job title", "description": "keyword1, keyword2, keyword3, ...", "start_date": "YYYY-MM", "end_date": "YYYY-MM or Present", "location": "City, Country"}}]}}

        RESUME TEXT:
        {text_resume}

        JSON OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = exp_prompt | llm | out_parser

    exp_analysis = chain.invoke({"text_resume": text_resume})

    return exp_analysis


def extract_projects(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting projects ...")
    proj_prompt = PromptTemplate.from_template(
        """You are an expert resume parser.

        TASK: Extract ALL project entries from the resume.

        For each project entry, extract:
        - Project name
        - Description: EXACTLY 5 keywords describing key responsibilities and technologies

        IMPORTANT RULES:
        1. Output ONLY valid JSON format
        2. No additional text, comments, or explanations
        3. Use exact field names as shown in the format
        4. Description must contain MAXIMUM 5 keywords separated by commas
        5. Keywords should focus on: technologies, tools, responsibilities, achievements
        6. If information is missing, use empty string ""
        7. No indentation or formatting

        OUTPUT FORMAT:
        {{"projects": [{{"name": "Project name", "description": "Responsibilities, acchievements, technologies, tools, and frameworks used"}}]}}

        RESUME TEXT:
        {text_resume}

        JSON OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = proj_prompt | llm | out_parser

    proj_analysis = chain.invoke({"text_resume": text_resume})

    return proj_analysis


def extract_skills(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting skills ...")
    skills_prompt = PromptTemplate.from_template(
        """You are an expert resume parser.

        TASK: Extract ALL skills from the resume.

        For each skill category, extract:
        - Programming languages and proficiency level
        - Technical skills and tools
        - Soft skills and competencies

        IMPORTANT RULES:
        1. Output ONLY valid JSON format
        2. No additional text, comments, or explanations
        3. Use exact field names as shown in the format
        4. Skills should include proficiency level when mentioned
        5. If information is missing, use empty array []
        6. No indentation or formatting

        OUTPUT FORMAT:
        {{"skills": [{{"name": "skill name", "proficiency": "skill proficiency}}]}}

        RESUME TEXT:
        {text_resume}

        JSON OUTPUT:"""
    )

    out_parser = StrOutputParser()

    chain = skills_prompt | llm | out_parser

    skills_analysis = chain.invoke({"text_resume": text_resume})

    return skills_analysis


def parse_topic(topic, llm, text_resume, max_failure):
    failing_c = 0
    topic_analysis = None
    while failing_c < max_failure:

        try:
            if topic == "education":
                topic_analysis = extract_education(llm, text_resume)
            elif topic == "experience":
                topic_analysis = extract_experience(llm, text_resume)
            elif topic == "projects":
                topic_analysis = extract_projects(llm, text_resume)
            elif topic == "skills":
                topic_analysis = extract_skills(llm, text_resume)
                print("skl \n", topic_analysis)
            else:
                raise NotImplementedError(f"topic {topic} was not found !")

            topic_analysis = parse_analysis(topic_analysis, topic)
            print("topic parsed \n", topic_analysis)
            topic_analysis = json.loads(topic_analysis)
            break

        except Exception as e:
            failing_c += 1
            print(f"Education extraction failed (attempt {failing_c}): {e}")

    return topic_analysis


def parse_analysis(topic_analysis: str, topic: str):
    topic_analysis = topic_analysis.strip()
    if topic in topic_analysis:
        start_idx = topic_analysis.find("[{")
        end_idx = topic_analysis.find("]}")

    return topic_analysis[start_idx : end_idx + 1]


def extract_profile(hf_api_key: str, text_resume: str, max_failure: int = 10):
    try:
        print("Text to analyze \n", text_resume)

        print("Loading the analyser ...")
        login(hf_api_key)
        model_id = "Qwen/Qwen3-4B"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline(
            "text-generation", model=model, tokenizer=tokenizer, return_full_text=False
        )
        llm = HuggingFacePipeline(
            pipeline=pipe,
        )

        combined_profile = {}
        topics = ["education", "experience", "projects", "skills"]
        # topics = ["skills"]
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, topic in enumerate(topics):
            status_text.text(f"Extracting {topic}...")
            topic_analysis = parse_topic(topic, llm, text_resume, max_failure)
            combined_profile[topic] = topic_analysis

            progress = (i + 1) / len(topics)
            progress_bar.progress(progress)

        status_text.text("Profile extracted!")
        return combined_profile

    except Exception as e:
        st.text("⚠️ Profile extraction failed, please try again")
