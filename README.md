# AWS CLoudFormation Cost-related Questions on Stack Overflow

## Requirements

To run **Step 1**, you will need a [Conda installation](https://docs.conda.io/projects/conda/en/stable/user-guide/install/download.html#anaconda-or-miniconda).

For **Step 2**, you can either use Conda or Docker. But if you use Conda, you must have Firefox installed to be able to export the charts.

## Skipping Data Extraction

Between downloading the necessary files and running the scripts, the data extraction takes a long time. If you do not want to replicate this process, you can decompress the file `step-1-output-bkp.7z` and proceed to the analysis (see **Step 2**). The decompression should create a directory `step-1-output/` with a subfolder `questions/` containing the question dataset. Each question is stored in a separate JSON file named after the question ID and contains:
- the question itself
- the comments on the question
- the post history of the question
- the answers to the question
- the comments on the answers
- the post history of the answers

## Step 1 - Data Extraction

### Download the StackOverflow data dump

Download the following 7z files from the [data dump](https://archive.org/details/stackexchange):
- `stackoverflow.com-Posts.7z`
- `stackoverflow.com-Comments.7z`
- `stackoverflow.com-PostHistory.7z`

We used the data dump from [2024-04-02](https://archive.org/details/stack-exchange-data-dump-2024-04-02).

Place the files in the `step-1-data/` directory and **do NOT decompress them**.

### Extract the questions about CloudFormation

1. Navigate to the `step-1-scripts/` directory
2. Create the conda environment
    ```bash
    conda env create -f env.yaml
    ```
3. Activate the conda environment
    ```bash
    conda activate so-cloudformation
    ```
4. Run the script below, uncommenting step-by-step
    ```bash
    python extractor.py
    ```
    1. Extract the questions
    2. Add comments to the questions
    3. Add post history to the questions
    4. Extract the answers
    5. Add comments to the answers
    6. Add post history to the answers
    7. Add answers to the questions and cleanup
5. Delete the conda environment
    ```bash
    conda deactivate && conda env remove -n so-cloudformation
    ```

## Step 2 - Data Analysis

### Start the JupyterLab server

1. Navigate to the `step-1-scripts/` directory
2. Start JupyterLab
    - Using conda
        1. Create the conda environment
            ```bash
            conda env create -f env.yaml
            ```
        2. Activate the conda environment
            ```bash
            conda activate so-cloudformation-notebook
            ```
        3. Start the server
            ```bash
            jupyter lab --port=8888 --no-browser --allow-root --LabApp.token='' --NotebookApp.notebook_dir='../'
            ```
    - Using Docker (if you have Docker installed)
        ```bash
        docker compose up
        ```
3. Open the JupyterLab server in your browser
    - [http://localhost:8888/lab](http://localhost:8888/lab)
4. Follow the instructions in the notebook `step-2-scripts/Cloudformation.ipynb`
5. Clean up the JupyterLab server:
    1. Stop the server (and container)
        ```bash
        CTRL+C
        ```
    2. Clean up
        - Using conda
            ```bash
            conda deactivate && conda env remove -n so-cloudformation-notebook
            ```
        - Using Docker
            ```bash
            docker compose down && docker rmi so-cloudformation-notebook
            ```
6. Follow the instructions in the notebook `step-3-scripts/topic-modelling.ipynb`
7. Stop the JupyterLab server and clean up
    1. Stop the server (and container)
        ```bash
        CTRL+C
        ```
    2. Clean up
        - Using conda
            ```bash
            conda deactivate && conda env remove -n so-cloudformation-notebook
            ```
        - Using Docker
            ```bash
            docker compose down && docker rmi so-cloudformation-notebook
            ```

## Dataset

The final dataset is available in the directory `step-2-output/questions/`. It contains the 218 questions about Cloudformation (i.e., one more tags matching `*cloudformation*`) with cost-related keywords. Each question is stored in a separate JSON file named after the question ID and contains:
- the question itself
- the comments on the question
- the post history of the question
- the answers to the question
- the comments on the answers
- the post history of the answers
- list of sentences mentioning one of the studies properties of the knowledge graph presented in the paper (fields `filtered-sentences`).

## Licenses

The software in this repository is licensed under the [MIT License](LICENSE).

The data compiled in this repository is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0) License.


