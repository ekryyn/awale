Simple network awale

To create server and wait for opponent :

	python awale.py


To join a game :

	python awale.py <host>

Protocol :
__TCP__

Message Structure as ASCII:

	SIZE\n\nJSONDATA

Where SIZE is the ASCII length of JSONDATA (A number)
and JSONDATA is a JSon Object with 2 attributes:

 - __type__: a string that could be :
   - info
   - game\_state
   - play
   - error
 - __message__: can be any valid json object


