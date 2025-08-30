import os

# Define project structure
project_structure = {
    "data": ["input.txt", "log_analyzer.py"],
    "data_gen": ["data_generator.py"],
    "docs": ["project_overview.md"],
    "src": ["mapper.py", "reducer.py", "run.sh"],
    "static": {
        "images": []
    },
    ".": ["README.md"],  # root-level files
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  
            # It's a folder with substructure
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):  
            # It's a folder with files
            os.makedirs(path, exist_ok=True)
            for file in content:
                file_path = os.path.join(path, file)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        f.write("")  # create empty file
        elif name == ".":  
            # root-level files
            for file in content:
                file_path = os.path.join(base_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        f.write("")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Current dir
    project_name = "ETralytica"
    root_path = os.path.join(base_dir, project_name)

    os.makedirs(root_path, exist_ok=True)
    create_structure(root_path, project_structure)

    print(f"Project structure for '{project_name}' created at {root_path}")
