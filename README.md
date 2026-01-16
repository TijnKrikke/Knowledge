# Knowledge Technology Practical

**Welcome to our project** 

This repository contains our knowledge base and models.
It hosts a game recommender system, in which the user is asked a series of questions to determine what game to recommend. The questions are asked through a user interface, implemented with Streamlit, where the user can select one of multiple answers to the question. 

**Prerequisites**

```
pip install -r requirements.txt
```
This script will let you download all the dependencies.


**How to run the Streamlit app**

Open a terminal in the working directory. Run the command **streamlit run src/streamlit.py** to see the base interface. Another way is to run the main.py file, which runs the command for you. If its the first time using Streamlit, you might need to accept some terms or give your e-mail.


**Structure**

```bash
├── resources/
│   ├── games.yml
│   ├── questions.yml
│   └── rules.yml
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

The main.py file is an easy way to boot up the streamlit. model.py contains all the classes used for our inference. parser.py contains a parser for the YAML knowledgebase. solver.py contains a solver with combined forward and backward chaining. streamlit_app.py contains the main streamlit page. The resources folder contains our knowledgebase. 