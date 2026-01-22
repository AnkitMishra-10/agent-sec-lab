from agent.core import run_agent

print("Agent Security Lab")
print("Type 'exit' to quit\n")

while True:
    user_input = input(">> ")
    if user_input.lower() == "exit":
        break
    run_agent(user_input)
