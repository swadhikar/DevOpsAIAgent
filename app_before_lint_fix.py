import os, re, subprocess
import json, datetime


def classify_log(log: str) -> dict:
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
    if os.path.exists(directory):
        return os.path.abspath(directory)
    return 'not found'


def summarize_directory_contents(path: str) -> list:
    files = []
    for dirpath, _, filenames in os.walk(path):
        for file in filenames:
            if file.endswith(".log") or file.endswith(".txt"):
                files.append(os.path.join(dirpath, file))
    return files


def check_python_version() -> str:
    version = subprocess.run(["python", "--version"], capture_output=True, text=True)
    return version.stdout.strip()


def count_lines_in_file(filepath: str) -> int:
    with open(filepath, "r") as f:
        return sum(1 for _ in f)


def cleanup_temp_files(directory: str) -> None:
    for file in os.listdir(directory):
        if file.endswith(".tmp") or file.startswith("~"):
            try:
                os.remove(os.path.join(directory, file))
            except:
                pass


def parse_json_string(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}


def convert_timestamp_to_iso(timestamp: float) -> str:
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.isoformat()
    except Exception as e:
        return str(e)


def find_errors_in_log(log_text: str) -> list:
    errors = []
    for line in log_text.splitlines():
        if "error" in line.lower() or "exception" in line.lower():
            errors.append(line.strip())
    return errors


def extract_imports(code_text: str) -> list:
    lines = code_text.splitlines()
    return [line for line in lines if line.strip().startswith("import") or line.strip().startswith("from")]
