# ElecCalc

Early prototype for TUMJA: Team Climates calculator project

Installation (Linux/ MacOS):

1. Install Anaconda according to you OS
2. cd into the directory you want to have the project located
3. Clone GitHub repository:  
    `git clone https://github.com/AlexHls/ElecCalc.git`
4. Install conda environment:  
    `conda env create --file eleccalc_env.yml`
5. Activate conda environment:  
    `conda activate eleccalc`
6. Change into the main directory (should contain a manage.py file)
7. Start the local server:  
    `python managy.py runserver`
8. If everything worked, you should see an adress in your command line output (something like localhost:8000). Click on it or paste it into your browsers adress line
9. Enjoy!

Installation (Windows):
1. Install Anaconda according to your OS
2. Open Anaconda Powershell Prompt (find it with Win+S)
3. Clone GitHub repository from ''
4. Install conda environment:  
    `conda env create --file eleccalc_env.yml`
5. Cone GitHub repository from `https://github.com/AlexHls/ElecCalc`
    1. You can use the GitHub for Windows Desktop Client
    2. You can use the builtin git manager in your IDE (e.g. PyCharm)
    3. Download the zip folder directly from the GitHub page and extract it
6. Select the newly created environment as python interpreter in you IDE of choice
   (I'm sure there is a way to execute it in the Anaconda Prompt, probably works similar
   to Linux/ MacOS).
7. Run `manage.py` (with your IDE or via `python managy.py runserver`)
8. Enjoy!
