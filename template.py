import os
from pathlib import Path

LIST_FILES = [
    # "Dockerfile",
    ".env",
    ".gitignore",
    "src/__init__.py",
    "src/utils/__init__.py",
    # "src/utils/mathcad_xml_2_latex_parser.py",
    # "src/utils/mathcad_symbol_parser.py",
   ]

for file_path in LIST_FILES:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)

    # first make dir
    if file_dir!="":
        os.makedirs(file_dir, exist_ok= True)
        print(f"Creating Directory: {file_dir} for file: {file_name}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path, "w") as f:
            pass
            print(f"Creating an empty file: {file_path}")
    else:
        print(f"File already exists {file_path}")