from agent.core import run_agent

def main():
    print("Agent Security Lab")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input(">> ")
        if user_input.lower() == "exit":
            print("Exiting.")
            break
        run_agent(user_input)

if __name__ == "__main__":
    main()
