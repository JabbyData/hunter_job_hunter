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
        """
    You are an expert resume parser. Extract education information from the provided resume text.

    INSTRUCTIONS:
    - Extract ALL education entries from the resume
    - For each education entry, identify: institution name, degree level, field of study, and dates
    - Output ONLY a valid JSON string with no additional text or explanations
    - Use consistent formatting and avoid duplicates
    - No identation

    OUTPUT FORMAT:
    {{
    "education": [
        {{
        "institution": "University/School name",
        "degree_level": "Bachelor's/Master's/PhD/Certificate/etc.",
        "field_of_study": "Major/Field/Specialization",
        "start_date": "YYYY or YYYY-MM",
        "end_date": "YYYY or YYYY-MM or 'Present'",
        "location": "City, Country (if available)"
        }}
    ]
    }}

    RESUME TEXT:
    {text_resume}

    JSON OUTPUT:
    """
    )

    out_parser = StrOutputParser()

    chain = educ_prompt | llm | out_parser

    edu_analysis = chain.invoke({"text_resume": text_resume})

    return edu_analysis


def extract_experience(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting experience ...")
    exp_prompt = PromptTemplate.from_template(
        """
    You are an expert resume parser. Extract work experience information from the provided resume text.

    INSTRUCTIONS:
    - Extract ALL professional experience entries from the resume
    - For each experience entry, identify: company name, position, key responsibilities/achievements, and employment dates
    - DESCRIPTION GUIDELINES:
      * Extract 5-10 most relevant keywords describing responsibilities, achievements, or technologies used
    - Output ONLY a valid JSON string with no additional text or explanations
    - Use consistent formatting and avoid duplicates
    - No indentation

    OUTPUT FORMAT:
    {{
    "experience": [
        {{
        "company": "Company name",
        "position": "Job title/Position",
        "description": "5-10 key responsibilities, achievements, or technologies",
        "start_date": "YYYY or YYYY-MM",
        "end_date": "YYYY or YYYY-MM or 'Present'",
        "location": "City, Country (if available)"
        }}
    ]
    }}

    RESUME TEXT:
    {text_resume}

    JSON OUTPUT:
    """
    )

    out_parser = StrOutputParser()

    chain = exp_prompt | llm | out_parser

    exp_analysis = chain.invoke({"text_resume": text_resume})

    return exp_analysis


def extract_projects(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting projects ...")
    proj_prompt = PromptTemplate.from_template(
        """
    You are an expert resume parser. Extract project information from the provided resume text.

    INSTRUCTIONS:
    - Extract ALL project entries from the resume
    - For each project entry, identify: project name and tools used
    - Output ONLY a valid JSON string with no additional text or explanations
    - Use consistent formatting and avoid duplicates
    - No identation

    OUTPUT FORMAT:
    {{
    "projects": [
        {{
        "name": "Project name",
        "tools": "Technologies, tools, and frameworks used",
        }}
    ]
    }}

    RESUME TEXT:
    {text_resume}

    JSON OUTPUT:
    """
    )

    out_parser = StrOutputParser()

    chain = proj_prompt | llm | out_parser

    proj_analysis = chain.invoke({"text_resume": text_resume})

    return proj_analysis


def extract_skills(llm: HuggingFacePipeline, text_resume: str):
    print("Extracting skills ...")
    skills_prompt = PromptTemplate.from_template(
        """
    You are an expert resume parser. Extract skills information from the provided resume text.

    INSTRUCTIONS:
    - Extract ALL skills mentioned in the resume
    - Categorize skills into technical skills, soft skills, and languages
    - Associate proficiency to skills
    - Identify soft skills by focusing on descriptions in the projects and experience sections
    - Output ONLY a valid JSON string with no additional text or explanations
    - Use consistent formatting and avoid duplicates
    - JSON format should be respected
    - No indentation

    OUTPUT FORMAT:
    {{
    "skills": [
        {{
        "Languages": ["language1/Beginner", "language2/Intermediate", "language3/Expert"]
        }},
        {{
        "Technical": ["skill1/Beginner", "skill2/Intermediate", "skill3/Expert"]
        }},
        {{
        "Soft Skills": ["skill1/Beginner", "skill2/Intermediate", "skill3/Expert"]
        }}
    ]
    }}

    RESUME TEXT:
    {text_resume}

    JSON OUTPUT:
    """
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
                print("exp : \n", topic_analysis)
            elif topic == "projects":
                topic_analysis = extract_projects(llm, text_resume)
            elif topic == "skills":
                topic_analysis = extract_skills(llm, text_resume)
            else:
                raise NotImplementedError(f"topic {topic} was not found !")

            topic_analysis = parse_analysis(topic_analysis, topic)
            topic_analysis = json.loads(topic_analysis)
            break

        except Exception as e:
            failing_c += 1
            print(f"Education extraction failed (attempt {failing_c}): {e}")

    return topic_analysis


def parse_analysis(topic_analysis: str, topic: str):
    topic_analysis = topic_analysis.strip()

    if "JSON OUTPUT:" in topic_analysis:
        topic_analysis = topic_analysis.split("JSON OUTPUT:")[-1].strip()
    if "{" in topic_analysis and topic in topic_analysis:
        start_idx = topic_analysis.find('{"' + topic + '"')
        end_idx = topic_analysis.find("]}")

    return topic_analysis[start_idx : end_idx + 2]


def extract_profile(hf_api_key: str, text_resume: str, max_failure: int = 10):
    try:
        print("Text to analyze \n", text_resume)

        print("Loading the analyser ...")
        login(hf_api_key)
        model_id = "Qwen/Qwen3-8B"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline(
            "text-generation", model=model, tokenizer=tokenizer, return_full_text=False
        )
        llm = HuggingFacePipeline(
            pipeline=pipe,
        )

        combined_profile = {}
        # topics = ["education", "experience", "projects", "skills"]
        topics = ["experience"]
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, topic in enumerate(topics):
            status_text.text(f"Extracting {topic}...")
            topic_analysis = parse_topic(topic, llm, text_resume, max_failure)
            combined_profile[topic] = topic_analysis[topic]

            progress = (i + 1) / len(topics)
            progress_bar.progress(progress)

        status_text.text("Profile extracted!")
        return combined_profile

    except Exception as e:
        st.text("⚠️ Profile extraction failed, please try again")
