# Discovery_AI_Powered_Platform
Discovery AI Powered Platform For Your Data Analysis &amp; Discovery


## Introduction



## What's This Project About?



## Why Use This Project?



## Architecture

The project consists of the following components:

1. Frontend: Streamlit Web Application
2. Backend: Flask Web Server with RESTful API
3. Services: LLM Service for property classification, Database Service for data management
4. External Components: Groq API for LLM model access
5. Data Storage: JSON file (company_db.json)

**Prerequisites:**
- Python installed on your system.
- A basic understanding of virtual environments and command-line tools.

**Steps:**
1. **Virtual Environment Setup:**
   - Create a dedicated virtual environment for our project:
   
     ```bash
     python -m venv Discovery_AI_Powered_Platform
     ```
   - Activate the environment:
   
     - Windows:
       ```bash
       Discovery_AI_Powered_Platform\Scripts\activate
       ```
     - Unix/macOS:
       ```bash
       source Discovery_AI_Powered_Platform/bin/activate
       ```
2. **Install Project Dependencies:**

   - Navigate to your project directory and install required packages using `pip`:
   
     ```bash
     cd path/to/your/project
     pip install -r requirements.txt
     ```

3. **Setup Keys : **

   - Obtain your Groq API key from [Groq Console](https://console.groq.com/keys).
   - Set your key in the `.env` file as follows:
   
     ```plaintext
    GROQ_API_KEY=<YOUR_KEY>       
    SERPER_API_KEY=KEY # https://serper.dev/     
    SEC_API_API_KEY=KEY # https://sec-api.io/ 
    
     ```

4. **Run the Market Analysis AI Application**

   Finally, execute the following command to start the Market Analysis AI application:

   ```bash   
   # Run UI
   streamlit run app\main.py
   ```  

