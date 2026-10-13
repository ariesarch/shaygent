# import argparse
# import os
# import json
# from dotenv import load_dotenv
# from openai import OpenAI
# from prompts import system_prompt
# from call_function import available_functions


# def main():
#     parser = argparse.ArgumentParser(description="Chatbot")
#     parser.add_argument("user_prompt", type=str, help="User prompt")
#     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
#     args = parser.parse_args()

#     load_dotenv()

#     api_key = os.environ.get("OPENROUTER_API_KEY")

#     if not api_key:
#         raise ValueError("OPENROUTER_API_KEY is missing from the .env file")

#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=api_key,
#     )
#     messages=[
#         {"role": "user","content": args.user_prompt},
#         {"role": "system", "content": system_prompt},
#     ]
#     response = client.chat.completions.create(
#         model="openrouter/free",
#         messages=messages,
#         tools=available_functions,
#         temperature=0,
#     )
#     if response.usage is None:
#         raise RuntimeError("API response does not contain token usage information")
#     if args.verbose:
#         print(f"User prompt: {args.user_prompt}")
#         print(f"Prompt tokens: {response.usage.prompt_tokens}")
#         print(f"Response tokens: {response.usage.completion_tokens}")
#         print()
#         # print("Response:")

#     message = response.choices[0].message

#     if message.tool_calls:
#         for tool_call in message.tool_calls:
#             function_args = json.loads(
#                 tool_call.function.arguments or "{}"
#             )
#             print(
#                 f"Calling function: "
#                 f"{tool_call.function.name}({function_args})"
#             )
#     else:
#         print(message.content)    


# if __name__ == "__main__":
#     main()

# import argparse
# import json
# import os

# from dotenv import load_dotenv
# from openai import OpenAI

# from call_function import available_functions, call_function
# from prompts import system_prompt


# load_dotenv()

# api_key = os.environ.get("OPENROUTER_API_KEY")

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=api_key,
# )


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("user_prompt", help="The prompt to send to the AI")
#     parser.add_argument(
#         "--verbose",
#         action="store_true",
#         help="Enable verbose output",
#     )
#     args = parser.parse_args()

#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": args.user_prompt},
#     ]

#     response = client.chat.completions.create(
#         model="openrouter/free",
#         messages=messages,
#         tools=available_functions,
#         temperature=0,
#     )

#     if response.usage is None:
#         raise RuntimeError("Response usage information is unavailable")

#     if args.verbose:
#         print(f"User prompt: {args.user_prompt}")
#         print(f"Prompt tokens: {response.usage.prompt_tokens}")
#         print(f"Response tokens: {response.usage.completion_tokens}")
#         print()

#     message = response.choices[0].message

#     if message.tool_calls:
#         for tool_call in message.tool_calls:
#             result_message = call_function(tool_call, args.verbose)

#             if not result_message["content"]:
#                 raise Exception("Function call returned empty content")

#             if args.verbose:
#                 print(f"-> {result_message['content']}")
#     else:
#         print(message.content)


# if __name__ == "__main__":
#     main()

import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

MAX_ITERATIONS = 20


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", help="The prompt to send to the AI")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        if args.verbose:
            if response.usage is not None:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(
                    f"Response tokens: "
                    f"{response.usage.completion_tokens}"
                )

        message = response.choices[0].message

        # Keep the assistant's response in the conversation history.
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(
                    tool_call,
                    args.verbose,
                )

                if not result_message.get("content"):
                    raise Exception("Function call returned empty content")

                # Return each tool result to the conversation history.
                messages.append(result_message)

                if args.verbose:
                    print(f"-> {result_message['content']}")

        else:
            print("Final response:")
            print(message.content)
            break

    else:
        print(
            f"Error: Agent reached the maximum number of "
            f"iterations ({MAX_ITERATIONS}) without a final response."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
