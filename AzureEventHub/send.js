const { EventHubProducerClient } = require("@azure/event-hubs");

const connectionString = "";
const eventHubName = "testhub";

async function main() {

  // Create a producer client to send messages to the event hub.
  const producer = new EventHubProducerClient(connectionString, eventHubName);

  // Prepare a batch of three events.
  const batch = await producer.createBatch();
  batch.tryAdd({ body: "First event" });
  batch.tryAdd({ body: "Second event" });
  batch.tryAdd({ body: "Third event" });
  batch.tryAdd({ body: "4" });
  batch.tryAdd({ body: "5" });
  batch.tryAdd({ body: "6" });
  batch.tryAdd({ body: "7" });
  batch.tryAdd({ body: "8" });
  batch.tryAdd({ body: "9" });
  batch.tryAdd({ body: "10" });

  // Send the batch to the event hub.
  await producer.sendBatch(batch);

  // Close the producer client.
  await producer.close();

  console.log("A batch of three events have been sent to the event hub");
}

main().catch((err) => {
  console.log("Error occurred: ", err);
});