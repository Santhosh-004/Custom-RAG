
def memoryExtenderMessage(prompt: str):
    message = f'''
            Instructions:
                Identify and classify each memory as either a fact or an event.
                A fact is a piece of permanent or unchanging information.
                An event is a time-bound action or state that may change over time.
                Nothing other than this like simple conversations to pass time or other things that are not facts or events should be labeled as simple_conversation.
                Categorize each memory as either a fact or an event.
            Examples:
                Prompt: "My name is Arjun."
                → fact
                Prompt: "I was born on January 5, 1998."
                → fact
                Prompt: "Hello there!"
                → simple_conversation
                Prompt: "What does the cosmos mean?"
                → simple_conversation
                Prompt: "I started working at Infosys in July 2022."
                → event
                Prompt: "I moved to Bangalore in March 2023."
                → event
                Prompt: "What is the meaning of life?"
                → simple_conversation
                Prompt: "My blood type is O positive."
                → fact
                Prompt: "What is the capital of India?"
                → simple_conversation
                Prompt: "When is your birthday?"
                → simple_conversation
                Prompt: "In August 2024, I joined Google as a software engineer."
                → event
                Prompt: "I am an Indian citizen."
                → fact
                Prompt: "How are you doing?"
                → simple_conversation
                Prompt: "What is your favorite color?"
                → simple_conversation
                Now, the user's prompt is: {prompt}
                → (The model should now output one of the following: fact, event, simple_conversation)
    '''
    return message

def queryAnswer(query: str, mem):
    message = f'''
            You are a helpful assistant created by Santhosh to be helpful to the user and help them in all possible ways. You will receive a lot of data in the form of a json object.
            The data contains a conversation memory, stored facts, and stored events.
            Your task is to answer the user's question using the conversation memory, stored facts, and stored events.
            If the user's question cannot be answered using the conversation memory, stored facts, and stored events, you should respond with "I don't know. But I will remember if you tell me from now" kinda response
            If the user's question can be answered using the conversation memory, stored facts, and stored events, you should respond as if you are having a conversation without  letting the user know you have the json object.
            Now, the user's question is: {query}
            The json object is: {mem}
        '''
    return message

def infoQuestionMessage(prompt: str):
    message = f'''
        You are a classification assistant.
        Your task is to read each message from the user and classify it as one of the following:
            question: if the user is asking something (even indirectly)
            information: if the user is just sharing a fact, event, or statement, and is not expecting an answer
            Respond only with the label: question or information.
            Examples:
                User: "Where did I store my file from last week?"
                → question
                User: "I joined Volante Technologies in 2025."
                → information
                User: "How do I set up a vector store?"
                → question
                User: "I moved to Bangalore in March 2024."
                → information
                User: "What’s the difference between facts and events?"
                → question
                User: "My favorite programming language is Python."
                → information
                User: "Hello there!"
                → chatter
                User: "what are you doing?"
                → chatter
                User: "how are you?"
                → chatter
            Now evaluate this new message from the user:
            User: "{prompt}"
            → (The model should now output just: question or information or chatter)
        '''
    return message