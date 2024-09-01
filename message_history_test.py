from message_history import MessageHistory

message_history = MessageHistory(database_name="history_test.db", current_conversation="1")

message_history.initialize()

message_history.create_new_conversation()

message_1 = {"message": "Hello", "sender": "user"}
message_2 = {"message": "Hello, how can I help you today?", "sender": "assistant"}

messages = [message_1, message_2]

for message in messages:
    message_history.insert_messages(message=message)

messages = message_history.get_messages()
print(messages)

message_history.info()
