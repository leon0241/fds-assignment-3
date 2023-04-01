import pandas as pd
import re

def remove_time_inc(df_row):
    reg = re.search("[0-9]*(?=\+)", df_row["time_control"])
    if reg != None:
        df_row["time_control"] = reg.group()
        # print(df_row["time_control"])
    return df_row

def import_data():
    '''
    Imports chess CSV file, cleans data, and returns an output pandas dataframe
    '''
    
    # todo: i forgor what the exact file is called, update this
    CHESS_DATA_LOCATION = "data/club_games_data.csv"
    # MOVIES_DATA_LOCATION = "data/movies.csv"

    # load csv into a big dataframe
    chess_data = pd.read_csv(CHESS_DATA_LOCATION)

    # Drops rows if any value is a NaN, but data is clean so it doesn't do anything
    chess_data.dropna(axis = 0, how = 'any')
    # filter out alternative rules like chess960 etc
    chess_data = chess_data[chess_data['rules'] == "chess"]
    # remove any game that starts with rnbqkbnr cos that shows the game barely developed
    chess_data = chess_data[chess_data['time_class'] != "daily"]
    
    
    chess_data = chess_data.apply(remove_time_inc, axis=1)

    chess_data = chess_data[~(chess_data['white_result'] == chess_data['black_result'])]

    # if the game ends with "rnbqkbnr", that indicates a very undeveloped board,
    # i.e. the game barely started so it shouldn't be counted
    chess_data = chess_data[~chess_data['fen'].str.startswith("rnbqkbnr/")]

    # get IDs of values to drop (so the for loop doesn't mess up )
    drops = []
    # preemptive index reset
    chess_data = chess_data.reset_index(drop=True)
    # for any in the chess data
    for i in range(len(chess_data)):
        # get pgn string (final line of pgn column)
        pgn = chess_data['pgn'][i].splitlines()[-1]
        # find all entries of a move
        # i.e. "1." or "2."
        entries = re.findall("[123456789]\.", pgn)
        
        filter_n = 5
        # for the second type of pgn, detect timestamps and
        # since moves are labelled 1. 1... 2. 2..., double the filter size
        if (re.search("\{\[.{12,13}\]\}",pgn) != None):
            # i.e. "1. g4 {[%clk 47:56:02]}"
            filter_n = 10

        # if there's less than 5 moves, then delete entry
        if (len(entries) < filter_n):
            # print(pgn)
            drops.append(chess_data.index[i])
            # chess_data = chess_data.drop(chess_data.index[i])
            # chess_data = chess_data.reset_index(drop=True)

    # drop every entry with a drop ID
    for drop_id in drops:
        chess_data = chess_data.drop(drop_id)
    chess_data = chess_data.reset_index(drop=True)
    
    return chess_data

