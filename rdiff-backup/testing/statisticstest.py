import unittest
execfile("commontest.py")
rbexec("statistics.py")

class StatsObjTest(unittest.TestCase):
	"""Test StatsObj class"""
	def set_obj(self, s):
		"""Set values of s's statistics"""
		s.SourceFiles = 1
		s.SourceFileSize = 2
		s.NewFiles = 3
		s.NewFileSize = 4
		s.DeletedFiles = 5
		s.DeletedFileSize = 6
		s.ChangedFiles = 7
		s.ChangedSourceSize = 8
		s.ChangedMirrorSize = 9
		s.IncrementFileSize = 10
		s.StartTime = 11
		s.EndTime = 12

	def test_get_stats(self):
		"""Test reading and writing stat objects"""
		s = StatsObj()
		assert s.get_stat('SourceFiles') is None
		self.set_obj(s)
		assert s.get_stat('SourceFiles') == 1

		s1 = StatsITR()
		assert s1.get_stat('SourceFiles') == 0

	def test_get_stats_string(self):
		"""Test conversion of stat object into string"""
		s = StatsObj()
		stats_string = s.get_stats_string()
		assert stats_string == "", stats_string

		self.set_obj(s)
		stats_string = s.get_stats_string()
		assert stats_string == \
"""StartTime 11
EndTime 12
SourceFiles 1
SourceFileSize 2
NewFiles 3
NewFileSize 4
DeletedFiles 5
DeletedFileSize 6
ChangedFiles 7
ChangedSourceSize 8
ChangedMirrorSize 9
IncrementFileSize 10""", "'%s'" % stats_string

	def test_init_stats(self):
		"""Test setting stat object from string"""
		s = StatsObj()
		s.init_stats_from_string("NewFiles 3 hello there")
		for attr in s.stat_attrs:
			if attr == 'NewFiles': assert s.get_stat(attr) == 3
			else: assert s.get_stat(attr) is None, (attr, s.__dict__[attr])

		s1 = StatsObj()
		self.set_obj(s1)
		assert not s1.stats_equal(s)

		s2 = StatsObj()
		s2.init_stats_from_string(s1.get_stats_string())
		assert s1.stats_equal(s2)

	def test_write_rp(self):
		"""Test reading and writing of statistics object"""
		rp = RPath(Globals.local_connection, "testfiles/statstest")
		if rp.lstat(): rp.delete()
		s = StatsObj()
		self.set_obj(s)
		s.write_stats_to_rp(rp)

		s2 = StatsObj()
		assert not s2.stats_equal(s)
		s2.read_stats_from_rp(rp)
		assert s2.stats_equal(s)


if __name__ == "__main__": unittest.main()