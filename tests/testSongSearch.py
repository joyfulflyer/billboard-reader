import unittest
from context import reader
import reader.songSearch as songSearch
from reader.song import Song

class TestSongSearch(unittest.TestCase):
    def test_remove_dupes(self):
        date = "date"
        artistName = "artiist"
        start = [
        Song(0, "firstName", artistName, date),
        Song(0, "secondName", artistName, date),
        Song(0, "firstName", artistName, date),
        Song(0, "secondName", "the artist formerly known as artiist", date)
        ]
        end = songSearch.removeDupes(start)
        self.assertEqual(end, [Song(0, "secondName", artistName, date), Song(0, "firstName", artistName, date), Song(0, "secondName", "the artist formerly known as artiist", date)])


    def test_song(self):
        self.assertNotEqual(Song(0, "first", "a", "5"), Song(0, "last", "e", "6"))

    def test_songs_by_name(self):
        artistName = "artiist"
        date = "date"

        start = [
        Song(0, "firstName", artistName, date),
        Song(0, "secondName", artistName, date),
        Song(0, "firstName", artistName, date),
        Song(0, "secondName", "the artist formerly known as artiist", date)
        ]
        end = songSearch.getSongsWithName(start, "tn")
        print(list(end))


if __name__ == '__main__':
    unittest.main()
