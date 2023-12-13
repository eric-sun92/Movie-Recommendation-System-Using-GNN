# CPSC-483-Final-Project

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python.
- You have a Windows/Linux/Mac machine.

## Installation 

### Setting up the Environment

To run this project, set up a Python environment and install the required packages. Both implementations have their own `requirements.txt` file.

#### Clone the Repository

```bash
git clone git@github.com:eric-sun92/CPSC-483-Final-Project.git
cd CPSC-483-Final-Project
```

#### Create a Python Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```
#### For Windows, activate the virtual environment:
```bash
.\venv\Scripts\activate
```

#### For Unix or MacOS, activate the virtual environment:
```bash
source venv/bin/activate
```

#### Install Required Packages
```bash
pip install -r requirements.txt
```

## To Run

1. Download the MovieLens-100K, MovieLens-1M, MovieLens-25m, and Book-Crossing datasets from their respective sources.
   - MovieLens: [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)
   - Book-Crossing: [https://www.kaggle.com/datasets/somnambwl/bookcrossing-dataset](https://www.kaggle.com/datasets/somnambwl/bookcrossing-dataset)
2. Move the unzipped files into the repository.
   - **Note**: Ensure to change the path in the notebooks to the correct path for the dataset.
3. Run all cells in the notebook.
