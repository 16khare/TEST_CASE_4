import json
import subprocess

def build_module(module, built_modules):
    if module in built_modules:
        print(f"Module {module} has already been built. Skipping.")
        return

    if ":" in module:
        group_id, artifact_id, version = module.split(":")
        command = f"mvn clean install -DgroupId={group_id} -DartifactId={artifact_id} -Dversion={version}"
    else:
        command = f"mvn clean install -DartifactId={module}"

    # Capture the output of the build command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Module {module} built successfully.")
        built_modules.add(module) # Add the module to the set of built modules
        print(result.stdout) # Print the build output
    else:
        print(f"Error building module {module}.")
        print(result.stderr) # Print any error output

# Initialize a set to keep track of built modules
built_modules = set()

with open("sorted_modules.txt") as f:
    for line in f:
        module = line.strip()
        if module:
            print(f"Building module: {module}")
            build_module(module, built_modules)
