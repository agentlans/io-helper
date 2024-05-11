# io-helper

A Python package to make reading and writing files easier.
Clearer and more concise syntax.

---

# Install

`pip install git+https://github.com/agentlans/io-helper.git`

# Use

```python

# Read lines of text file
f = TextFile("/tmp/file.txt")
for line in f:
	print(f)
f.close()

# JSON example
j = JSONLFile("/tmp/foo.json", 'w')
j.write([1,2,3])
j.close()

# SQLite example
db = SQLite("/tmp/foo.db")
db.execute("CREATE TABLE Foo (a INT, b TEXT)")
db.execute("INSERT INTO Foo VALUES (?,?)", 1, "hello")
db.commit()
for x in db.query("SELECT * FROM Foo"):
	print(x)
db.close()
```

# Author, Licence

Copyright :copyright: 2024 by Alan Tseng
GNU General Public Licence 3.0