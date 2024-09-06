# File Organizer

File Organizer is a simple Python script that helps you organize files in a
specified folder based on their extensions. It also identifies and moves
duplicate files to a separate folder.

## Features

- Organizes files into subfolders based on their extensions
- Detects and moves duplicate files to a "Duplicates" folder
- Provides a summary and detailed report of the organization process

## Requirements

- Python 3.6 or higher

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency
management. If you haven't installed Poetry yet, please follow the [official
installation guide](https://python-poetry.org/docs/#installation).

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```
   poetry install
   ```

   This command creates a virtual environment (if it doesn't exist) and installs
   all the required dependencies specified in the `pyproject.toml` file.

## Development

To activate the virtual environment for development:

```
poetry shell
```

This will spawn a new shell subprocess, which is configured to use the virtual
environment.

## Usage

Run the script from the command line:

```
python main.py
```

Follow the prompts to enter the path of the folder you want to organize.

## Project Structure

- `file_organizer.py`: Contains the `FileOrganizer` class with the main logic
  for organizing files
- `main.py`: The entry point of the application, handles user input and runs the
  file organizer

## How It Works

1. The script scans all files in the specified folder
2. It creates subfolders for each file extension encountered
3. Files are moved to their respective extension folders
4. If a duplicate file is found (based on MD5 hash), it's moved to the
   "Duplicates" folder
5. After organization, a report is generated showing the number of files moved
   and their destinations
