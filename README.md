Note this is just an experiement to learn how agentic coding applications work and doesnt comprise any production ready scafolding. Please test with a pinch of salt.

Place your API key in .env with the var name GEMINI_API_KEY = '** YOUR API KEY **'.

And use - uv run " ** Custom Prompt ** " --verbose
* An example of a custom prompt could be "Give me the first 5 fibonocci numbers using fib.py".
* The agentic system is expected to first validate if a python function already exists in fib.py, opens it and reads the contents and then execute it with the args required.
* The optional --verbose arg gives you other details such as token usage and agent context

The agent has 4 tool calling capabilities
1. Ability to scan folder structure
2. Ability to read files
3. Ability to write to files
4. Ability to run python files as a subprocess
