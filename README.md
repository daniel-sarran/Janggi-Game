# Janggi-Game
JanggiGame.py is a backend implementation of the Korean board game, Janggi!

Never heard of Janggi? That's alright! 

It's <i>mostly</i> like Chess, in the same way a crepe is <i>mostly</i> like a pancake.

There are some subtle differences in terms of how the pieces move, the ability of players to <i>pass</i>, and a special movement area of the game board called "the palace". But otherwise, each player is trying to put the opposing General ('King') in checkmate!

This implementation movement logic of each piece, including passing, capturing, blocking, check, etc.

The user interface is quite simple:
1) Create a `JanggiGame` class
2) Use the `make_move` method and pass the `from` and `to` square using algebraic notation (e.g. 'a1' or 'd10')
3) Continue until one player wins!

<img src="https://github.com/daniel-sarran/Janggi-Game/blob/main/images/Low_Level_IO.PNG" width="600">
