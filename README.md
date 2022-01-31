# ElecCalc

Early prototype for TUMJA: Team Climates calculator project

### Installation (Linux/ MacOS):

1. Install Anaconda according to you OS
2. cd into the directory you want to have the project located
3. Clone GitHub repository:  
    `git clone https://github.com/AlexHls/ElecCalc.git`
4. Install conda environment:  
    `conda env create --file eleccalc_env.yml`  
   *Note for MacOS: This should work as the yml file just specifies some packages to be specifically installed, letting your anaconda package manager deal with all the dependencies. In case it fails (e.g. at the same point as the Windows procedure during the matplotlib install, follow the manual install instructions in the Windows section.*
5. Activate conda environment:  
    `conda activate eleccalc`
6. Change into the main directory (should contain a manage.py file)
7. Start the local server:  
    `python manage.py runserver`
8. If everything worked, you should see an adress in your command line output (something like localhost:8000). Click on it or paste it into your browsers adress line
9. Enjoy!

### Installation (Windows):  
*Note: As it is with Windows there might be various problems along the way and there might be a more elegant way to install it, but this is the way I tested it and it worked.*
1. Install Anaconda according to your OS
2. Cone GitHub repository from `https://github.com/AlexHls/ElecCalc`
    1. You can use the GitHub for Windows Desktop Client
    2. You can use the builtin git manager in your IDE (e.g. PyCharm)
    3. Download the zip folder directly from the GitHub page and extract it  
3. Open Anaconda Powershell Prompt (find it with Win+S)
4. Try to install conda environment:  
    `conda env create --file eleccalc_env.yml`  
    1. In case it fails try manually creating the environment by running this series of commands:  
    `conda create --name eleccalc python=3.9`  
    `conda activate eleccalc`
    `conda install numpy`  
	`conda install scipy`
	`conda install corner`
    `conda install pandas`  
     `conda install django`  
     `conda install matplotlib` <- in case this fails run: `pip install matplotlib`  
    2. If you encounter any further problems or just want to be on the safe side (if you're on a system with an Intel CPU), install:  
    `conda install -c intel mkl-service`
6. Select the newly created environment as python interpreter in you IDE of choice
7. Run `manage.py` (either via the Anaconda Powershell Prompt by executing `python manage.py runserver` (recommended), or through your IDE)
8. Enjoy!
