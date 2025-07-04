from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from commands import get_available_linters, execute_command

from dotenv import load_dotenv

if load_dotenv("../../.env"):
    print("Environment variables loaded successfully.")

# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)


@tool
def get_linters() -> list:
    """Returns a list of available linters or formatters."""
    return get_available_linters()


@tool
def run_shell_command(command: str) -> str:
    """Executes a shell command and returns status and output."""
    return execute_command(command)


tools = [get_linters, run_shell_command]

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are CodeFixer, a code-fixing assistant. Your job is to fix Python linting and formatting issues by choosing the most appropriate tool from the list and executing it ONLY when needed.\n\n"
     "Tool usage guidelines:\n"
     """IMPORTANT: You must run all commands using the full syntax: `python -m <tool> app.py`. Do not omit `python -m`.
     For example:
     - Correct: `python -m autoflake --in-place app.py`
     - Incorrect: `autoflake app.py` ❌"""
     "Use `python -m <tool> <script.py>` for running tools\n"
     "- Feel free to use multiple tools in multiple iterations if needed to achieve maximum lint score \n"
     "- Use `autoflake` for unused imports or variables\n"
     "- Use `black` or `autopep8` for formatting\n"
     "- Use `pylint` or `flake8` only for checking, not fixing\n"
     "- NEVER call `echo` or write files — assume `app.py` already exists\n"
     "- NEVER call tools that don't help solve the actual issue\n\n"
     "- If you used tools that edited the code in place, please run linting tools to ensure formatting\n\n"
     "Use `get_linters()` to see available tools.\n"
     "Only call `run_shell_command()` with a valid command that actually fixes the listed errors."
     "Ensure to call the pylint command to spot the improvement in linting errors"
     ),
    ("human", (
        "A Python script called `app.py` has issues from pylint\n"
        "You have the following tools available: get_linters (lists available linters/formatters) and run_shell_command (executes commands).\n\n"
        "Your task is to:\n"
        "1. Call `get_linters`\n"
        "2. Choose the best tool\n"
        "3. Construct a shell command using the tool relevant to errors identified (e.g. `black app.py or autoflake app.py`) and call `run_shell_command with arguments`\n"
        "4. Return the result of the command.\n\n"
        "ONLY use tools that are available.\n"
        "Do not describe what you'd do — do it.\n"
    )),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

if __name__ == '__main__':
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke({})
