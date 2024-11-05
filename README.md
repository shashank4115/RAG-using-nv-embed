Steps to run the project
1. Create a new python environment using
    python -m venv "environment name"
2. Activate the python environment using
    .\"environment name"\Scripts\activate
3. once activated clone the git repository
4. Install the requirements.txt file
5. install Ollama from Llama website ollama.com
6. install Llama 3.1 8B or 70B based on system specification (use 8B if you have 16B ram and use 70B if you have 64GB or more ram)
    ollama run llama3.1:8b (for 8B parameter model)
    ollama run llama3.1:70b (for 70B parameter model)
8. in terminal run the app.py file
    streamlit run app.py
