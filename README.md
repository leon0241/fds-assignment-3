# fds-assignment-3

## Importing the dataset
Put the `.csv` file into `.\data` for the program to work properly

- [Link to dataset (Kaggle.com)](https://www.kaggle.com/datasets/adityajha1504/chesscom-user-games-60000-games)

- [Direct mirror to CSV (OneDrive)](https://uoe-my.sharepoint.com/:f:/g/personal/s2202694_ed_ac_uk/Eht2Vq26VG1EjXjnz3wL6rkB2JgYYlPw_-jtvzLpkVJp6w?e=eStOrq)

## Required Python libraries
- `re` for regex string parsing
- `pandas` for dataframes
- `pandarallel` for multi-core dataframe processing
- `chess` for PGN parsing
- `seaborn` and `matplotlib` for data visualisation
- `scikit-learn` for data processing and machine learning

## Helper files
- `data_cleaning.py`: imports the csv file and cleans the data
- `stockfish_eval.py`: class with functions to evaluate a board state