<h3>Google Cloud Pub/Sub</h3>
https://cloud.google.com/pubsub/docs/
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Global-scale message buffer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;No-ops
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Auto-Scaling
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Guaranteed at-least-once delivery
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Cloud Pub/Sub is a global service (PubSub’s servers run in multiple data centers)
<br>
<br><b><a href="https://cloud.google.com/pubsub/docs/authentication">Authentication</a></b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Service accounts are recommended for almost all use cases
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;You can authenticate users directly to your application (app access on behalf of user)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;IAM can be configured at the project level and at the individual resource level.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Grant access on a <b>per-topic</b> or <b>per-subscription</b> basis
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Grant access with <b>limited capabilities</b> ie. only publish messages
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Grant access with <b>limited capabilities</b> ie. only consume messages
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Grant access to all Cloud Pub/Sub resources within a project to a group of developers.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Permission Methods  -  projects.subscriptions.xxxx
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Permission Methods  -  projects.topics.xxxx
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Roles:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Primitive Roles (Owner, Editor, Viewer)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;pubsub.admin
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;pubsub.publisher
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;pubsub.subscriber
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;pubsub.viewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;pubsub.editor
<br>
<br><b>Publisher</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Creates and sends messages to a topic
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Guaranteed at-least-once delivery
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Best-effort ordering (In general, doesn't care about order. Order handled in Dataflow)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;When using JSON over REST, message data must be base64-encoded
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Messages must be smaller than 10MB (after decoding)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Note that the message payload must not be empty
<br>
<br><b>Subscriber</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Must create a subscription to that topic, in order to receive published messages.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;A topic can have multiple subscriptions
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;A given subscription belongs to a single topic.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;By default, a message not delivered within 7 days is deleted (range: 10 min to 7 days)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Once a message is sent to a subscriber, the subscriber must either ack or drop the message
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Pull Subscription</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Subscriber initiates requests to the Pub/Sub server to retrieve messages
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... Large volume of messages (batch delivery)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... Efficiency and throughput of message processing is critical.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... HTTPS endpoint, w/ non-self-signed SSL certificate, isnt feasible.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Push Subscription</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;PubSub sends msg as HTTPS request to subscriber app @ preconfigured endpoint
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... Lower latency (more real-time) required
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... Google Cloud dependencies (such as creds) are not feasible
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... Multiple topics that must be processed by the same webhook
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use when... App Engine Standard subscribers.
<br>
<br><b>References:</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<a href="https://cloud.google.com/pubsub/docs/">Google Cloud Pub/Sub Docs</a>
