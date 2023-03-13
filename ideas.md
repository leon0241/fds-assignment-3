### Chess
- en passant and percentages of wins (meme idea)

    = Can en passant move at any point in the game predict whether player is more likely to win
    Follow up Q: Predicting ELO from whether en passant moves were taken where possible???
        Predicting whether en passant move will be chosen where possible based on board position AND ELO
- castling and percentages of wins
    = Does castling kingside vs queenside vs not at all for black and white predict whether player is more likely to win
    Follow up Q: Is it possible to predict which side you'll castle based on opening?
- "You could also choose to take a ‘deep-dive’ into one of the features (e.g. the “time control”) to
analyse their apparent influence on the game.": Analyse game mode (blitz, rapid etc) to see how fast a big blunder is made

- likelihood to win following a big blunder ( speed chess)
    - predicting elo from blunders
    - comparing different time classes of chess per player (blunders in each type, ie does number of blunders in longer time control predict number of blunders in shorter time control)

###### Columns to work with
| white_rating | black_rating | white_result | black_result | time_class | time_control | rules | rated | fen | pgn
| - | - | - | - | - | - | - | - | - | - |

### Movie


###### Significant moves
- en passant
- castle
- promotion
- capture a queen
- (fork, pin etc) is_pinned()

- Does using a significant move affect likelihood of winning/ does number of significant moves
in a game affect likelihood of winning

- Follow up: Is it possible to predict ELO based on which significant moves are used and when?
