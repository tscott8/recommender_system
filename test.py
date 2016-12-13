from file_handler import FileHandler 


fh = FileHandler()
# found = False
found, artist = fh.check_for_file('Radioactive')
print("Artist: ", artist)
if found:
    print("File exists!")
    data = fh.retrieve_file('Radioactive', artist)
    print("data: ", data)
else:
    print("File doesn't exist...")

