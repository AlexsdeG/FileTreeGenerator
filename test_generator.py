import os
import shutil
import subprocess
from pathlib import Path

def setup_test_environment():
    """Creates a temporary directory structure for testing."""
    test_dir = Path("test_project")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()

    (test_dir / "file1.txt").touch()
    (test_dir / ".hidden_file.txt").touch()

    folder1 = test_dir / "folder1"
    folder1.mkdir()
    (folder1 / "subfile1.txt").touch()

    subfolder1 = folder1 / "subfolder1"
    subfolder1.mkdir()

    folder2 = test_dir / "folder2"
    folder2.mkdir()
    (folder2 / "file2.log").touch()
    (folder2 / ".hidden_folder").mkdir()

    return test_dir

def run_test(args, test_name):
    """Runs the main script with given arguments and checks the output."""
    print(f"--- Running Test: {test_name} ---")
    try:
        command = ["python", "main.py"] + args
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {test_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILURE: {test_name}")
        print(f"Error: {e.stderr}")
        return False

def cleanup(test_dir):
    """Removes the test directory and exports."""
    shutil.rmtree(test_dir)
    exports_dir = Path("exports")
    if exports_dir.exists():
        shutil.rmtree(exports_dir)
    print("\nCleanup complete.")

def main():
    test_dir = setup_test_environment()
    all_tests_passed = True
    
    # Test 1: Generate text file with depth 1
    args1 = [str(test_dir), "-o", "tree_depth1.txt", "-d", "1"]
    if not run_test(args1, "Text output with depth 1"):
        all_tests_passed = False
    
    # Test 2: Generate markdown with directories only
    args2 = [str(test_dir), "-o", "tree_dirs.md", "-f", "markdown", "-D"]
    if not run_test(args2, "Markdown output with directories only"):
        all_tests_passed = False

    # Test 3: Generate JSON excluding 'folder1'
    args3 = [str(test_dir), "-o", "tree_exclude.json", "-f", "json", "--exclude", "folder1"]
    if not run_test(args3, "JSON output excluding a folder"):
        all_tests_passed = False

    # Test 4: Show hidden files
    args4 = [str(test_dir), "-o", "tree_hidden.txt", "--show-hidden"]
    if not run_test(args4, "Text output including hidden files"):
        all_tests_passed = False

    print("\n--- Verifying generated files ---")
    exports = Path("exports")
    expected_files = ["tree_depth1.txt", "tree_dirs.md", "tree_exclude.json", "tree_hidden.txt"]
    for f in expected_files:
        if (exports / f).is_file():
            print(f"Verified: '{f}' exists.")
        else:
            print(f"Verification FAILED: '{f}' does not exist.")
            all_tests_passed = False
            
    cleanup(test_dir)
    
    if all_tests_passed:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    main()