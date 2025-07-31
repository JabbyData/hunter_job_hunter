"""
Module to implement a matchmaker agent
"""

import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import subprocess
import time


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
            {{"job_title": job title,
            "industry": industry,
            "city": city,
            "country": country
            "job_type": job type,
            "seniority": entry level,
            "min_salary": min salary,
            "max_salary": max salary,
            "education": EDUCATION LIST,
            "experience": EXPERIENCE LIST,
            "skills": SKILL LIST}}
            
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

        Task : Compare entries from USER_PROFILE and SEARCH_CRITERIA with the ones of STRUCTURED_JOB_INFO and decide if the candidate is a good match for the job.

        IMPORTANT RULES:
            0. "-1" values are not comparable, skip them.
            1. USER_PROFILE, SEARCH_CRITERIA and STRUCTURED_JOB_INFO are presented as hashmap : an entry is a couple key/value.
            1. For each entry, compare values from USER_PROFILE or SEARCH_CRITERIA to the value of the corresponding key in STRUCTURED_JOB_INFO.
            # TODO : OCNTINUE
    
        """
    )


def filter_jobs(user_profile: dict, search_criteria: dict, jobs: pd.DataFrame) -> float:
    """
    Brief description of what the function does.

    Args:
        arg_1 (str): Description of the first parameter.
        arg_2 (np.array): Description of the second parameter.
        arg_n (int)(optional): Description of the third parameter.

    Returns:
        float: Description of the return value.

    Raises:
        ExceptionType: Description of the exception that might be raised.

    Example:
    >>> filter_jobs(arg_1, arg_2, arg_n)
    expected_output
    """

    try:
        subprocess.Popen(
            ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(2)
    except Exception as e:
        print(f"Failed to start Ollama server: {e}")

    llm = OllamaLLM(model="gemma3:27b")

    selected_jobs = []
    for i, job_description in enumerate(jobs["description"]):
        print(f"Analyzing job {i}...")
        structured_job_info = extract_job_info(job_description, llm)
        print(structured_job_info)

        # if match_job_profile(user_profile, search_criteria, structured_job_info):
        #     print("Good job !")

    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False)
        time.sleep(2)
    except Exception as e:
        print(f"Failed to kill Ollama server: {e}")


if __name__ == "__main__":
    jobs = pd.read_csv("src/data/jobs.csv")
    jobs = jobs[
        [
            "job_url_direct",
            "title",
            "company",
            "location",
            "job_type",
            "job_level",
            "description",
        ]
    ].iloc[:2]
    filter_jobs(user_profile=None, jobs=jobs, search_criteria=None)
    # TODO : compute to dict + match user profile
