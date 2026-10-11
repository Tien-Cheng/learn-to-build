import sys
with open(sys.argv[1], "rb") as f:
    header = f.read(100)
size = int.from_bytes(header[16:18], "big")
print("%-20s %d" % ("database page size:", 65536 if size == 1 else size))
