# Knowledge Technology Practical

**Welcome to our project** 

This repository will contain our knowledge base and models.

**Prerequisites**

```
pip install -r requirements.txt
```
This script will let you download all the dependencies.


**How to run the Streamlit app**

Open a terminal in the working directory. Run the command **streamlit run src/streamlit.py** to see the base interface.


**Structure**

```bash
├── resources/
│   └── kb.yml
├── src/
│   ├── main.py
│   ├── model.py
│   ├── parser.py
│   ├── solver.py
│   ├── streamlit_app.py
├── .gitignore
├── README.md
├── requirements.txt
```

The main.py file is an easy way to boot up the streamlit. model.py contains all the classes used for our inference. parser.py contains a parser for the YAML knowledgebase. solver.py contains a solver with forward chaining. streamlit.py contains the main streamlit page, which is our UI for getting information from the user.