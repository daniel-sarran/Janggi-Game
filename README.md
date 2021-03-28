# Janggi-Game
JanggiGame.py is a backend implementation of the Korean board game, Janggi!

Never heard of Janggi? That's alright! (You could check out this <a href="https://en.wikipedia.org/wiki/Janggi">Wikipedia</a> page for more information)

It's <i>mostly</i> like Chess, in the same way a crepe is <i>mostly</i> like a pancake.

There are some subtle differences in terms of how the pieces move, the ability of players to <i>pass</i>, and a special movement area of the game board called "the palace". 

Nonetheless, each player is trying to put the opposing General ('King') into checkmate!

This implementation handles all movement logic of each piece, including passing, capturing, blocking, check, etc. There are two players: Blue and Red, where Blue starts.

The user interface is quite simple:
1) Create a `JanggiGame` class
2) Use the `make_move` method and pass the `from` and `to` square using algebraic notation (e.g. 'a1' or 'd10') -- if the move is valid, `make_move` returns True, and `False` otherwise.
3) Continue until one player wins!

<code>game = JanggiGame()
  
game.make_move('a7', 'a6') # Blue player moves

game.make_move('c1', 'd3') # Red player moves

<img src="https://github.com/daniel-sarran/Janggi-Game/blob/main/Janggi_Screenshot.png" width="600">

