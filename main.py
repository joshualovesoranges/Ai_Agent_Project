import ollama
from tools import web_search



def run_agent():
    """
    Run the AI agent in a loop, taking user input and generating responses.
    """
    #messages to keep track of the conversation history
    messages = [{
        "role": "system",
        "content": (
            "You have exactly one tool available: web_search. No other tools exist. "
            "Only call web_search for questions about real-world events, facts, or "
            "data from 2024 or later that you cannot answer from general knowledge "
            "(examples: sports results, news, current prices, recent releases). "
            "Never call web_search for math, logic, definitions, or general knowledge "
            "questions. Basic math facts are always certain. Do not call web_search "
            "for arithmetic under any circumstances. "
            "Answer directly in plain text whenever you already know the answer. "
            "Never invent a tool that isn't web_search. "
            "Treat search results as more accurate than your own knowledge when you do search. "
            "If a question is ambiguous, briefly mention both interpretations "
            "and answer each if the results allow."
    )
    }]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for up-to-date information. Use this when the user asks about current events, recent information, or information you are unsure about.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to send to the web."
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]


    # Main loop for running the agent and handling user input
    while True:

        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        while True:
            response = ollama.chat(
                model="qwen2.5:7b",
                messages=messages,
                tools=tools
            )

            message = response.message

            messages.append(message)

            if not message.tool_calls:
                break

            # If the message contains tool calls, we need to process them before breaking out of the loop.
            for call in message.tool_calls:
                if call.function.name == "web_search":
                    query = call.function.arguments.get("query")
                    result = web_search(query)
                    
                else:
                    result = f"Unknown tool call: {call.function.name}"

                messages.append({
                    "role": "tool",
                    "tool_name": call.function.name,
                    "content": result
                })


        print("AI:", message.content)


if __name__ == "__main__":
    run_agent()
