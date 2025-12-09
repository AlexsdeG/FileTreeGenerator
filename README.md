### FileTreeGenerator - A Python File Structure Tree Generator

Tool to generate formatted file and folder structures in text, markdown and json formats. It allows output in the console or saving to a file. No need for installation, just run the script with your local installed Python version directly.


![App Screenshot](https://github.com/AlexsdeG/FileTreeGenerator/blob/main/FileTreeGenerator.png)

#### Features

*   Generate file and folder structures in three formats: text, markdown, and json.
*   Command-line interface (CLI) for easy usage.
*   Options to customize output, including depth, directory-only view, hidden files, and exclusions.
*   Save output to a file in an `exports` directory or print to the console.
*   Cross-platform compatibility (Windows, macOS, Linux).
*   No installation required, just run with Python. Uses only standard Python libraries for maximum compatibility.
*   Includes a test script to verify functionality.


### 1. Project Structure

The project will be organized into the following file structure:

```
filetreegenerator/
├── main.py
├── test_generator.py
└── exports/
```

*   `main.py`: The main script containing the `TreeGenerator` class and the command-line interface logic.
*   `test_generator.py`: A separate script for testing the functionality of `main.py`.
*   `exports/`: A directory where the generated file tree outputs will be saved. This directory will be created by the script if it doesn't exist.


#### 2. Command-Line Interface (CLI)

The CLI is implemented using the `argparse` module.

**Usage:**

```bash
python main.py [path] [options]
```

**Arguments:**

*   `path` (optional): The root directory. If not provided, the script will prompt for it.
*   `-o`, `--output` (optional): The name of the output file to be saved in the `exports` directory. If not provided, the tree is printed to the console.
*   `-d`, `--depth` (optional, default: -1): The maximum recursion depth. `-1` means unlimited.
*   `-f`, `--format` (optional, default: 'text'): The output format. Can be `'text'`, `'markdown'`, or `'json'`.
*   `-D`, `--dir-only` (optional, action: 'store_true'): Only include directories in the tree.
*   `--show-hidden` (optional, action: 'store_true'): Include hidden files and directories.
*   `--exclude` (optional, nargs='+'): A space-separated list of file or directory names to exclude.

#### 3. Output Formats

*   **Text (`text`):** A classic tree structure using UTF-8 characters.
    ```
    .
    ├── file1.txt
    ├── folder1
    │   ├── subfile1.txt
    │   └── subfolder1
    └── folder2
        └── file2.txt
    ```
*   **Markdown (`markdown`):** A nested list that renders correctly in Markdown.
    ```markdown
    *   .
        *   file1.txt
        *   folder1
            *   subfile1.txt
            *   subfolder1
        *   folder2
            *   file2.txt
    ```
*   **JSON (`json`):** A nested dictionary representing the file structure.
    ```json
    {
      "name": ".",
      "type": "directory",
      "contents": [
        {
          "name": "file1.txt",
          "type": "file"
        },
        {
          "name": "folder1",
          "type": "directory",
          "contents": [
            {
              "name": "subfile1.txt",
              "type": "file"
            },
            {
              "name": "subfolder1",
              "type": "directory",
              "contents": []
            }
          ]
        },
        {
          "name": "folder2",
          "type": "directory",
          "contents": [
            {
              "name": "file2.txt",
              "type": "file"
            }
          ]
        }
      ]
    }
    ```
