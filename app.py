import os
import subprocess
import json
import datetime


def classify_log(log: str) -> dict:
    """
    Classifies the type of error from a given log string.

    Args:
        log (str): The log content to analyze.

    Returns:
        dict: A dictionary with error_type, summary, and suggested_fix.
    """
    log = log.lower()

    if "modulenotfound" in log or "importerror" in log:
        error_type = "dependency_error"
        summary = "missing python module detected"
        suggested_fix = "Install the required dependency using pip."
    elif "assertionerror" in log or "test failed" in log:
        error_type = "test_failure"
        summary = "A test case failed during execution."
        suggested_fix = "Check test assertions and expected outputs."
    elif "connection timed out" in log:
        error_type = "infra_error"
        summary = "Network timeout or infrastructure issue."
        suggested_fix = "Check network/firewall or cloud resources."
    else:
        error_type = "unknown"
        summary = "Could not identify a specific failure pattern."
        suggested_fix = "Review the full log manually."

    return {"error_type": error_type, "summary": summary, "suggested_fix": suggested_fix}


def get_absolute_path(directory: str) -> str:
    """
    Returns the absolute path of a given directory if it exists.

    Args:
        directory (str): The target directory path.

    Returns:
        str: Absolute path or 'not found'.
    """
    if os.path.exists(directory):
        return os.path.abspath(directory)
    return 'not found'


def summarize_directory_contents(path: str) -> list:
    """
    Recursively finds all .log and .txt files in a directory.

    Args:
        path (str): The directory to search.

    Returns:
        list: A list of paths to log or text files.
    """
    files = []
    for dirpath, _, filenames in os.walk(path):
        for file in filenames:
            if file.endswith(".log") or file.endswith(".txt"):
                files.append(os.path.join(dirpath, file))
    return files


def check_python_version() -> str:
    """
    Returns the current Python version as a string.

    Returns:
        str: The output of `python --version`.
    """
    version = subprocess.run(["python", "--version"],
                             capture_output=True, text=True)
    return version.stdout.strip()


def count_lines_in_file(filepath: str) -> int:
    """
    Counts the number of lines in a file.

    Args:
        filepath (str): Path to the file.

    Returns:
        int: Number of lines in the file.
    """
    with open(filepath, "r") as f:
        return sum(1 for _ in f)


def cleanup_temp_files(directory: str) -> None:
    """
    Deletes temporary files (e.g., .tmp, ~files) in the given directory.

    Args:
        directory (str): Path to the directory to clean.
    """
    for file in os.listdir(directory):
        if file.endswith(".tmp") or file.startswith("~"):
            try:
                os.remove(os.path.join(directory, file))
            except:
                pass


def parse_json_string(json_str: str) -> dict:
    """
    Parses a JSON string into a Python dictionary.

    Args:
        json_str (str): JSON-formatted string.

    Returns:
        dict: Parsed dictionary or error info if invalid.
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}


def convert_timestamp_to_iso(timestamp: float) -> str:
    """
    Converts a Unix timestamp into ISO 8601 format.

    Args:
        timestamp (float): Unix timestamp.

    Returns:
        str: ISO formatted date string.
    """
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.isoformat()
    except Exception as e:
        return str(e)


def find_errors_in_log(log_text: str) -> list:
    """
    Extracts lines containing 'error' or 'exception' from a log.

    Args:
        log_text (str): The complete log text.

    Returns:
        list: A list of error-related lines.
    """
    errors = []
    for line in log_text.splitlines():
        if "error" in line.lower() or "exception" in line.lower():
            errors.append(line.strip())
    return errors


def extract_imports(code_text: str) -> list:
    """
    Extracts import statements from Python source code.

    Args:
        code_text (str): The full Python source code.

    Returns:
        list: A list of import statements.
    """
    lines = code_text.splitlines()
    return [line for line in lines if line.strip().startswith("import") or line.strip().startswith("from")]
