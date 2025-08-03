<img src="logo.png" width="400">

**HJH** is an agentic AI assistant helping finding jobs.

###  How it works 
1. Upload your **PDF Resume** (should contain sections "education", "experience", "projects" and "skills").
2. An agent extracts key elements from your profile.
3. **HJH** then recommends you related jobs you might be interested in.
4. The assistant is asking you to specify your **search criteria**.
5. Antoher agent finds relevant **opportunities** associated with your profile and criteria.
6. **HJH** finally displays filtered jobs that are a good match for you.

### Installation

#### Models configuration

The original implementation of this project works with local **Ollama** models.
You can adapt it to meet your GPU capabilities by pulling specific models and editing the following instances (replace the model name with yours): 

```python
llm = OllamaLLM(model="gemma3:27b")
```

For moore details about **Ollama**, please visit https://github.com/ollama/ollama.

#### Environment setup

The original project runs under python 3.11. Here is the script to setup the environment using conda :

```
conda create -n hjh python=3.11
conda activate hjh
pip install -r requirements.txt
```

### Usage

To execute the code you just need to run the following command:

```bash
streamlit run src/main.py
```

It will then create a **streamlit** local host to interact with. If you want to upload a new PDF file, simply refresh the page.