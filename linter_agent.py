from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from commands import get_available_linters, execute_command
from docstring_agent import fix_docstring_errors
from model import openai_model, genai_model


@tool
def get_linters() -> list:
    """Returns a list of available linters or formatters."""
    return get_available_linters()


@tool
def run_shell_command(command: str) -> str:
    """Executes a shell command and returns status and output."""
    return execute_command(command)

@tool
def fix_docstrings(code_file: str, lint_error: str) -> str:
    """
    Given the script file path as a string and lint errors, adds docstrings
    and returns the code as string
    """
    return fix_docstring_errors(code_file, lint_error)


tools = [get_linters, run_shell_command, fix_docstrings]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are CodeFixer, a Python code-fixing assistant. Your task is to resolve linting and formatting issues by "
         "selecting and executing the most appropriate tools from the available list.\n\n"

         "📌 Tool Usage Guidelines:\n"
         "- You must run all tools using the exact syntax: "
         "`python -m <tool> app.py`. Do not omit `python -m`.\n"
         "  Examples:\n"
         "      Correct: `python -m autoflake --in-place app.py`\n"
         "      Incorrect: `autoflake app.py`\n\n"
         "  - Use `autoflake` to remove unused imports or variables.\n"
         "  - Use `black` or `autopep8` for formatting and code style fixes.\n"
         "  - Use `pylint` or `flake8` strictly for **checking**, not fixing.\n"
         "  - You may run multiple tools in multiple iterations if needed to achieve a high lint score.\n"
         "  - After using tools that make in-place changes (like `autoflake`, `black`, or `autopep8`), you must re-run `pylint` to verify improvements.\n"
         "  - For docstring missing errors, you may make use of tool `fix_docstrings` to make changes in place\n"
         "  - Never use `echo` or modify files manually. Assume `app.py` exists already.\n"
         "  - Do not call tools that are not related to the current errors.\n\n"
         "  Available tools: "
         "    `get_linters()` to view available linters/formatters and "
         "    `run_shell_command()` to execute shell commands.\n\n"
         "  Required Reporting:\n"
         "    - You must run `python -m pylint app.py` **before** and **after** fixing.\n"
         "    - Compare the linting outputs and summarize the improvement in a markdown table (Before vs After).\n"
         "    - Do not describe the command — execute it directly using `run_shell_command()`."
         ),
        ("human", (
            "The script `app.py` has linting issues reported by pylint.\n\n"
            "Please:\n"
            "1. Call `get_linters` to see what tools are available.\n"
            "2. Choose and apply the most relevant tools to fix the reported issues.\n"
            "3. Run `python -m pylint app.py` before and after fixing to verify improvements.\n"
            "4. Report the result as a markdown table comparing the two lint outputs.\n"
            "5. ONLY use tools that are available, and do not just describe your steps — actually execute the commands."
        )),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])


def fix_linting_errors():
    openai_agent = create_tool_calling_agent(openai_model, tools, prompt)
    agent_executor = AgentExecutor(agent=openai_agent, tools=tools, verbose=True)
    agent_executor.invoke({})

def fix_doc_string_errors():
    agent = create_tool_calling_agent(genai_model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor.invoke({})


if __name__ == '__main__':
    # fix_linting_errors()
    fix_doc_string_errors()
