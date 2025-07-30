"""
Module to implement a matchmaker agent
"""

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import subprocess
import time


def extract_job_info(job_description: str, llm: OllamaLLM):

    job_prompt = ChatPromptTemplate.from_template(
        """You are an expert analyst.

        TASK: Extract the following information from the job description :
            0. Job title.
            1. Industry,  business area the job is dealing with.
            2. City location.
            3. Country location.
            4. Job type : should be converted into one of the following values ["fulltime", "parttime", "internship", "contract].
            5. Job level : should be converted into one of the following values ["internship", "entry-level", "mid-senior level", "executive"].
            6. Minimum salary.
            7. Maximum salary.
            8. Highest degree level (should be one of the following values ["BSc","MSc","PhD"]) of the candidate associated with the area.
            10. Details about experience in a specific area : name of area + duration (in years).
            11. All the skills associated with their proficiency level (beginner, intermediate or fluent).
            
        IMPORTANT RULES:
            1. If value are missing, replace them with -1.
            2. Respect the output format. Do not use extra explanation.
            3. To fill output fields, use values from the job description ONLY.
        
        OUTPUT FORMAT:
            {{
                "job_title": "ai engineer",
                "industry": "technology",
                "city": "Paris",
                "country": "France",
                "job_type": "fulltime",
                "job_level": "entry-level",
                "min_salary": 3000,
                "max_salary": 5000,
                "degree_level": [("MSc","Data Science")],
                "experience": [("Software engineering",2),("Data scientist",1)],
                "skills": [("English","Fluent"),("Pytorch","Intermediate"),("Git","beginner")]
            }}
            
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

def match_job_profile(user_profile: dict , search_criteria: dict, structured_job_info: dict):
    pass

def filter_jobs(user_profile: dict,  search_criteria: dict, jobs: pd.DataFrame) -> float:
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

        if match_job_profile(user_profile,search_criteria,structured_job_info)

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
