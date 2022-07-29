from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://servicebus1zhuoran.servicebus.chinacloudapi.cn/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Cu+DOOOh4CSzFzXtfBSFDX/kQcL1XuAWkNdpHVhUWZg="
QUEUE_NAME = "queuetest"


def send_single_message(sender):
    # create a Service Bus message
    message = ServiceBusMessage("Single Message")
    # send the message to the queue
    sender.send_messages(message)
    print("Sent a single message")


def send_a_list_of_messages(sender):
    # create a list of messages
    messages = [ServiceBusMessage("Message in list") for _ in range(5)]
    # send the list of messages to the queue
    sender.send_messages(messages)
    print("Sent a list of 5 messages")


def send_batch_message(sender):
    # create a batch of messages
    batch_message = sender.create_message_batch()
    for _ in range(10):
        try:
            # add a message to the batch
            batch_message.add_message(ServiceBusMessage(
                "Message inside a ServiceBusMessageBatch"))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    # send the batch of messages to the queue
    sender.send_messages(batch_message)
    print("Sent a batch of 10 messages")


# create a Service Bus client using the connection string
servicebus_client = ServiceBusClient.from_connection_string(
    conn_str=CONNECTION_STR, logging_enable=True)
with servicebus_client:
    # get a Queue Sender object to send messages to the queue
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    with sender:
        # send one message
        send_single_message(sender)
        # send a list of messages
        send_a_list_of_messages(sender)
        # send a batch of messages
        send_batch_message(sender)

print("Done sending messages")
print("-----------------------")

with servicebus_client:
    # get the Queue Receiver object for the queue
    receiver = servicebus_client.get_queue_receiver(
        queue_name=QUEUE_NAME, max_wait_time=5)
    with receiver:
        for msg in receiver:
            print("Received: " + str(msg))
            # complete the message so that the message is removed from the queue
            receiver.complete_message(msg)
