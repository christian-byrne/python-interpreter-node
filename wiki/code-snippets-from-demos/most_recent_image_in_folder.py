import os
import random

files = os.listdir("/path/to/folder")

# Full paths

files = [os.path.join("/path/to/folder", f) for f in files]

files.sort(key=os.path.getmtime)

# Choose a random second image with the condition that it must be the same size
sample_files = [f for f in files if os.path.getsize(f) == os.path.getsize(files[1])]
paired_file = random.choice(sample_files)

image2.to(paired_file) # Wrapper class will handle conversion to tensor automatically