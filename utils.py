
def message_check(text):
    if not text or not text.strip():
        return True

def message_back(text):
    if text.lower() == 'отмена':
        return True