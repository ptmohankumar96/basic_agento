import os
import sys
from dotenv import load_dotenv
import argparse as ap
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

parser = ap.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

from google.genai import types

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


for _ in range(20):

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents= messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            ),
    )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if args.verbose:
        print(f'User prompt: {args.user_prompt}')

        prompt_tokens = response.usage_metadata.prompt_token_count
        print('Prompt tokens: '+str(prompt_tokens))

        response_tokens = response.usage_metadata.candidates_token_count
        print('Response tokens: '+str(response_tokens))

    function_responses = []

    if response.function_calls is not None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise RuntimeError("Result is empty")
            
            if function_call_result.parts[0].function_response is None:
                raise RuntimeError("Part[0] - Function response is None")
            
            if function_call_result.parts[0].function_response.response is None:
                raise RuntimeError("Part[0] - Function response.response is None")
            
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            function_responses.append(function_call_result.parts[0])
      
    else:
        print(response.text)
        sys.exit()

    messages.append(types.Content(role="user", parts=function_responses))


