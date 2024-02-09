from lyricsgenius import Genius

genius = Genius("HKtIlU3CSjM8tfVPmBYS59hu7o633x96FRNCsnayK_oxXU7lFOJ_QU5a5gMWb_-x")

artist_name = input("Enter the name of the artist: ")
song_number = int(input("Enter number of songs: "))


artist = genius.search_artist(artist_name, max_songs=song_number, sort="title")
print(artist.songs)