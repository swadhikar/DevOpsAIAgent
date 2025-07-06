from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from model import genai_model


def _get_comments_fixer_prompt() -> ChatPromptTemplate:
    system_prompt = """You are an intelligent python developer cum assistant.

        Important instructions:
        1. Given the python code as text, add docstrings to all the objects wherever necessary
        2. Only add comments to objects that does not contain docstrings
        3. Do not change any other part of code
        4. properly log the diffs at the end
        5. The code should be in proper python format and should job contain any formatting of sort ```python 
        """

    human_prompt = """Given the below python script and linting errors, please fix the fixable docstrings
        and return the code as text

        Lint errors:
        {lint_errors}

        Code:
        {code_as_text}
        """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", human_prompt)
        ]
    )

    return prompt


def fix_docstring_errors(filename: str, lint_error: str):
    prompt = _get_comments_fixer_prompt()
    chain = prompt | genai_model | StrOutputParser()
    with open(filename) as f:
        response = chain.invoke({"code_as_text": f.read(), "lint_errors": lint_error})

    with open(filename) as f:
        f.write(response)
        print(f'Written {filename} with corrected docstrings')


if __name__ == '__main__':

    lint = """************* Module projects.DevOpsAIAgent.app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:3:0: C0410: Multiple imports on one line (json, datetime) (multiple-imports)
app.py:82:14: W1510: 'subprocess.run' used without explicitly defining the value for 'check'. (subprocess-run-check)
app.py:96:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
app.py:96:32: C0103: Variable name "f" doesn't conform to snake_case naming style (invalid-name)
app.py:111:12: W0702: No exception type(s) specified (bare-except)
app.py:144:11: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:142:8: C0103: Variable name "dt" doesn't conform to snake_case naming style (invalid-name)
app.py:144:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)

-----------------------------------
Your code has been rated at 8.62/10
"""
    with open('./app_before_lint_fix.py') as f:
        resp = get_comments_fixed(f.read(), lint)

    print(resp)