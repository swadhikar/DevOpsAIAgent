import subprocess


AVAILABLE_LINTERS = [
    'pylint',       # ✅ correct
    'flake8',
    'black',
    'autopep8',
    'isort',
    'autoflake'
]

def get_available_linters() -> list:
    """
    Returns a list of available linters.
    """
    return ", ".join(AVAILABLE_LINTERS)

def execute_command(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    output = result.stdout.strip() + "\n" + result.stderr.strip() if result.stderr is not None else ""
    return output.strip()


if __name__ == "__main__":
    cmd = "python -m pylint app.py"
    result = execute_command(cmd)
    print(result)
