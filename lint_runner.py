# lint_runner.py (or fix_tools.py)
import subprocess
from typing import Dict, Any

# ... (keep your apply_autopep8_fixes function) ...

def apply_autoflake_fixes(file_path: str, remove_all_unused_imports: bool = True) -> Dict[str, Any]:
    """
    Applies autoflake fixes to a Python file in-place, primarily for removing unused imports.
    Set `remove_all_unused_imports` to True for aggressive removal (recommended for linting fixes).
    """
    try:
        command = [r'C:\Users\swadh\anaconda3\python.exe', '-m', 'autoflake', '--in-place']
        if remove_all_unused_imports:
            command.append('--remove-all-unused-imports')
        # You might also add --remove-unused-variables if Pylint flags them
        # command.append('--remove-unused-variables')
        command.append(file_path)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 or "no changes" in result.stderr.lower():
            return {"status": "success", "message": f"autoflake applied to {file_path}. {result.stderr.strip()}", "stderr": result.stderr.strip()}
        else:
            return {"status": "failed", "message": f"autoflake failed for {file_path}. Stderr: {result.stderr.strip()}", "stdout": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "autoflake command not found. Ensure it's installed (`pip install autoflake`) and in your PATH."}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred while running autoflake: {str(e)}"}


def apply_isort_fixes(file_path: str) -> Dict[str, Any]:
    """
    Applies isort to sort and organize imports in a Python file in-place.
    This often includes removing unused imports as a side effect.
    """
    try:
        result = subprocess.run(
            ['isort', file_path], # isort modifies in-place by default
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return {"status": "success", "message": f"isort applied to {file_path}. {result.stderr.strip()}", "stderr": result.stderr.strip()}
        else:
            return {"status": "failed", "message": f"isort failed for {file_path}. Stderr: {result.stderr.strip()}", "stdout": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "isort command not found. Ensure it's installed (`pip install isort`) and in your PATH."}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred while running isort: {str(e)}"}
    
    
if __name__ == "__main__":
    # Example usage
    file_path = "app.py"
    print(apply_autoflake_fixes(file_path))
    # print(apply_isort_fixes(file_path))