from ai.chatbot import chatbot

def test_chatbot():
    # Provide initial state (question only)
    inputs = {"question": "Show me failed login attempts", "context": "", "answer": ""}
    
    result = chatbot.invoke(inputs)
    print("Answer:", result["answer"])
    print("Context used:", result["context"])

if __name__ == "__main__":
    test_chatbot()
