import json
import os
import subprocess
from lxml import etree

def get_git_repo_root():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        raise IOError('Current working directory is not a git repository')

def parse_pom(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        namespace = {'mvn': 'http://maven.apache.org/POM/4.0.0'}

        groupId_elem = root.find('mvn:groupId', namespace)
        artifactId_elem = root.find('mvn:artifactId', namespace)
        version_elem = root.find('mvn:version', namespace)

        # Check if elements exist before accessing their text
        groupId = groupId_elem.text if groupId_elem is not None else None
        artifactId = artifactId_elem.text if artifactId_elem is not None else None
        version = version_elem.text if version_elem is not None else None

        dependencies = root.findall('.//mvn:dependency', namespace)

        module_info = {
            'groupId': groupId,
            'artifactId': artifactId,
            'version': version,
            'dependencies': [
                {
                    'groupId': dep.find('mvn:groupId', namespace).text if dep.find('mvn:groupId', namespace) is not None else None,
                    'artifactId': dep.find('mvn:artifactId', namespace).text if dep.find('mvn:artifactId', namespace) is not None else None,
                    'version': dep.find('mvn:version', namespace).text if dep.find('mvn:version', namespace) is not None else None,
                }
                for dep in dependencies
            ],
            'path': os.path.dirname(file_path),
            'buildCommand': 'mvn clean install'
        }
        return module_info
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def analyze_dependencies(directory):
    dag = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'pom.xml':
                file_path = os.path.join(root, file)
                module = parse_pom(file_path)
                if module is None:
                    continue
                key = f"{module['groupId']}:{module['artifactId']}:{module['version']}"
                if key not in dag:
                    dag[key] = module
    return dag

def main():
    try:
        directory = get_git_repo_root()
        dag = analyze_dependencies(directory)
        if dag:
            with open('build_dag.json', 'w') as f:
                json.dump(dag, f, indent=4)
            print("JSON file created successfully.")
        else:
            print("No valid pom.xml files found or all pom.xml files are missing required elements.")
    except IOError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()














