import csv
import json
import sqlite3

class File:
	def __init__(self, filename, mode='r', encoding='utf-8'):
		self.file = open(filename, mode=mode, encoding=encoding)
	def close(self):
		self.file.close()
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

class TextFile(File):
	def __init__(self, filename, mode='r', encoding='utf-8'):
		# Inherit all the methods and properties
		super().__init__(filename, mode=mode, encoding=encoding)
	def __iter__(self):
		return self
	def __next__(self):
		"Returns the next line in the file."
		line = self.file.readline()
		if line == "":
			raise StopIteration
		else:
			return line.strip()
	def read(self):
		"Read all the text from the current position to the end as a string."
		return self.file.read()
	def write(self, txt):
		"Writes string to file."
		self.file.write(str(txt))
	def write_line(self, txt, line_ending="\n"):
		"Writes a string to file as a single line."
		TextFile.write(self, txt)
		TextFile.write(self, line_ending)

class CSVFile(File):
	def __init__(self, filename, mode='r', **kwargs):
		"Opens a CSV file. Any extra arguments passed via kwargs."
		self.file = open(filename, mode=mode, newline="")
		try:
			self.reader = csv.reader(self.file, **kwargs)
			self.writer = csv.writer(self.file, **kwargs)
		except:
			pass
	def __iter__(self):
		return self
	def __next__(self):
		"Returns the next line in the CSV file."
		return next(self.reader)
	def write(self, lst):
		"Writes a single line to the CSV file."
		self.writer.writerow(lst)

# A JSON lines file
class JSONLFile(TextFile):
	def __init__(self, filename, mode='r'):
		super().__init__(filename, mode=mode)
	def __next__(self):
		"Reads an entry from the JSON file."
		return json.loads(TextFile.__next__(self))
	def write(self, obj, ensure_ascii=False, line_ending="\n"):
		"Writes an entry to the JSON file."
		js = json.dumps(obj, ensure_ascii=ensure_ascii)
		TextFile.write_line(self, js, line_ending)

# SQLite database
class SQLite:
	def __init__(self, filename):
		self.con = sqlite3.connect(filename)
		self.cur = self.con.cursor()
	def close(self):
		self.con.close()
	def execute(self, sql, *args):
		"Executes SQL code with the arguments. Assumes changes to the database."
		self.cur.execute(sql, args)
	def query(self, sql, *args):
		"Queries database with the SQL code and arguments and then returns result."
		# Make a new cursor
		cur = self.con.cursor()
		res = cur.execute(sql, args)
		return res
	def query_one(self, sql, *args):
		"Queries database with the SQL code and arguments and then returns one row."
		r = self.query(sql, *args)
		return r.fetchone()
	def commit(self):
		"Commit changes to the database after execute."
		self.con.commit()
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()
