import unittest
import songSearch
from song import Song

class TestSongSearch(unittest.TestCase):
	def testRemoveDupes(self):
		date = "date"
		artistName = "artiist"
		start = [
		Song(0, "firstName", artistName, date),
		Song(0, "secondName",artistName, date), 
		Song(0, "firstName", artistName, date), 
		Song(0, "secondName", "the artist formerly known as artiist", date)
		]
		end = songSearch.removeDupes(start)
		self.assertEqual(end, [Song(0, "secondName", artistName, date), Song(0, "firstName", artistName, date), Song(0, "secondName", "the artist formerly known as artiist", date)])


	def testSong(self):
		self.assertNotEqual(Song(0, "first", "a", "5"), Song(0, "last", "e", "6"))




if __name__ == '__main__':
	unittest.main()