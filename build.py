import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        sys.exit(result.returncode)
    print("Command completed successfully\n")

def main():
    """Build and publish the package to PyPI"""
    print("Starting build and publish process...")
    
    # Ensure we have the latest build tools
    run_command("pip install --upgrade pip setuptools wheel twine")
    
    # Remove any existing build directories
    if os.path.exists("dist"):
        print("Removing old dist directory...")
        run_command("rm -rf dist")
    
    if os.path.exists("build"):
        print("Removing old build directory...")
        run_command("rm -rf build")
    
    if os.path.exists("hashtagAI.egg-info"):
        print("Removing old egg-info directory...")
        run_command("rm -rf hashtagAI.egg-info")
    
    # Build source and wheel distributions
    print("Building distributions...")
    run_command("python setup.py sdist bdist_wheel")
    
    # Check the package
    print("Checking package...")
    run_command("twine check dist/*")
    
    # Upload to PyPI
    upload_choice = input("Do you want to upload to PyPI? (yes/no): ").lower()
    if upload_choice == 'yes' or upload_choice == 'y':
        print("Uploading to PyPI...")
        run_command("twine upload dist/*")
        print("Package published successfully to PyPI!")
    else:
        print("Upload canceled. Distribution files are available in the 'dist' directory.")
    
    print("\nBuild and publish process completed!")

if __name__ == "__main__":
    main()
