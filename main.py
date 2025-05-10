from memory_fusion import MemoryFusionEngine

if __name__ == '__main__':
    engine = MemoryFusionEngine()
    print("Smart Assistant ready. Type 'exit' to quit.")
    while True:
        text = input('You: ')

        if text.lower() in ['exit', 'quit']:
            break

        res = engine.process_user_input(text)
        print(f"Assistant: {res}")
        