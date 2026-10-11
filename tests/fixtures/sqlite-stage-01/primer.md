# Stage 01: `.dbinfo` prints the database page size

## What you're building

Your program reads a real SQLite database file, made by real SQLite, and reports the page size recorded in that file. It runs the way the real CLI does: one database file and one command.

```
$ python3 main.py sample.db .dbinfo
database page size:  4096
```

For a database created with `PRAGMA page_size=512`:

```
$ python3 main.py small.db .dbinfo
database page size:  512
```

For a database created with `PRAGMA page_size=65536`:

```
$ python3 main.py big.db .dbinfo
database page size:  65536
```

You can check any of these against the real thing with `sqlite3 sample.db .dbinfo`. The real CLI prints about 20 more lines. You can print the others too if you like, but this Stage checks only the page-size line.

## Interface contract

- **Invocation:** `python3 main.py <database-file> .dbinfo`. There are exactly two arguments.
- **The line:** `database page size:` padded on the right with spaces to 20 characters, then one space, then the page size in decimal. This is C's `"%-20s %d\n"`, so the label (19 characters) is followed by **2 spaces**: `database page size:  4096`.
- **Other lines:** allowed. The tests pick out the one stdout line that starts with `database page size:` and compare it exactly, so print that line only once.
- **Output rules:** stdout only, and every line ends with `\n`, including the last. No banner and no prompt.
- **Exit code:** `0`.
- **Read-only:** open the file for reading only. Never create or modify it.
- **Value:** the page size comes from the file's header (see Concepts). It is a power of two from 512 to 65536.

Missing files, non-SQLite files and unknown commands come in a later Stage. For now, assume the file is valid and the command is `.dbinfo`.

## Concepts

### A database is one file of fixed-size pages

The whole SQLite database (every table, index and the schema) is one ordinary file ([about.html](https://www.sqlite.org/about.html)). That file is split into **pages**, all the same size. Every structure SQLite stores (tables, indexes, the schema itself) is made of whole pages. Pages are numbered from 1, so page N starts at byte `(N - 1) * page_size` ([fileformat2.html §1.2 "Pages"](https://www.sqlite.org/fileformat2.html#pages)).

The page size is not fixed by the format. Anything from 512 to 65536 bytes is allowed, as long as it is a power of two. It is chosen when the database is created (`PRAGMA page_size=N` before the first table) and stays the same after that ([pragma.html#pragma_page_size](https://www.sqlite.org/pragma.html#pragma_page_size)). Every later step of a reader depends on this number: you cannot find page 2 until you know where page 1 ends. That is why it is the first thing you read. Hard-coding 4096, the usual default, works until someone hands you a file made with another setting.

### The 100-byte database header

The first 100 bytes of page 1 are the **database header**. It describes the file as a whole ([fileformat2.html §1.3 "The Database Header"](https://www.sqlite.org/fileformat2.html#the_database_header)). The fields you need now:

| Offset | Size | Meaning |
|---|---|---|
| 0 | 16 | the magic string `"SQLite format 3\0"` (15 ASCII characters, then a zero byte) |
| 16 | 2 | the page size |

There are more fields after these, for the page count, text encoding and so on. Later Stages use some of them.

You can see the header for yourself. This is a file with one table and the default page size:

```
$ xxd -l 32 one.db
00000000: 5351 4c69 7465 2066 6f72 6d61 7420 3300  SQLite format 3.
00000010: 1000 0101 0040 2020 0000 0001 0000 0002  .....@  ........
```

Offset 16 is the first two bytes of the second row: `10 00`.

### Big-endian integers

Every multi-byte integer in a SQLite file is **big-endian**: the most significant byte comes first ([fileformat2.html §1.3](https://www.sqlite.org/fileformat2.html#the_database_header)). So the two bytes `10 00` mean `0x10 * 256 + 0x00 = 4096`, and `02 00` means 512. Many CPUs, including x86 and ARM in their usual mode, store integers little-endian in memory, so the byte order has to be stated explicitly when a program decodes a file format. On-disk and network formats usually choose big-endian ("network byte order") so that a file means the same thing on every machine.

### Why 65536 is stored as `1`

Two unsigned bytes hold values from 0 to 65535, so 65536 does not fit. When SQLite 3.7.1 (2010) raised the maximum page size from 32 KiB to 64 KiB ([changes.html, 3.7.1](https://www.sqlite.org/changes.html)), it kept the file format compatible by giving the field a special value: **the stored value `1` means 65536** ([fileformat2.html §1.3.2 "Page Size"](https://www.sqlite.org/fileformat2.html#page_size)). The value 1 could never be a real page size, so nothing earlier became ambiguous. The real CLI handles it with one special case before printing (`if( i==1 ) i = 65536;`, [shell.c.in](https://github.com/sqlite/sqlite/blob/version-3.45.0/src/shell.c.in#L6272-L6274)).

```
$ xxd -s 16 -l 2 big.db
00000010: 0001
```

The same trick appears again later in the format: a "start of cell content area" of 0 in a page header also means 65536. Wherever your reader turns these bytes into a page size, the special case needs to be applied there. If it isn't, a 64 KiB file decodes as page size 1 and every page offset you compute afterwards is wrong.

### Making fixtures

You can make test files with Python's own `sqlite3` module, which is real SQLite:

```python
import sqlite3
c = sqlite3.connect("small.db")
c.execute("PRAGMA page_size=512")   # must come before the first CREATE
c.execute("CREATE TABLE t (id integer primary key, name text)")
c.commit()
c.close()
```

Name fixture files with a `.db` ending. Since 3.53, the `sqlite3` CLI runs arguments ending in `.sql` or `.txt` as scripts.

## Tests

- `.dbinfo` on a database made with default settings prints `database page size:  4096`.
- `.dbinfo` prints `database page size:  512` for a database with the smallest page size.
- `.dbinfo` prints the right page size for 1024, 2048, 8192, 16384 and 32768-byte pages.
- `.dbinfo` prints `database page size:  65536` for a file whose header stores the page size as 00 01.
- Three files of identical size (16384 bytes) with 2048, 4096 and 8192-byte pages each report their own page size.
- The `database page size:` line is byte-for-byte the same as the real `sqlite3` CLI's for 512, 4096 and 65536.
- `.dbinfo` output ends with a newline, including the last line.

Every test also checks that the exit code is 0. The oracle test needs the `sqlite3` CLI on your PATH.

## Done when

`./ltb test` prints `green`.
