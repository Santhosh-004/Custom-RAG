from enum import Enum

class PromptType(Enum):
    INFO = 1
    QUESTION = 2
    CHATTER = 3

class MemoryType(Enum):
    FACT = 1
    EVENT = 2
    SIMPLE_CONVERSATION = 3