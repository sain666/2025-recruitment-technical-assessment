# DevSoc Subcommittee Recruitment: Platforms
Your task is to send a direct message to the matrix handle `@chino:oxn.sh` using the Matrix protocol. However, this message must be sent over a self hosted instance such as through the Conduwuit implementation or the slightly more complicated Synapse implementation.

For this to work your server must be federated, but you do not have to worry about specifics such as using your domain name as your handle (a subdomain will do!) or have other 'nice to have' features. Just a message will do!

**You should write about what you tried and your process in the answer box below.**

This task intentionally sounds challenging and contains language not frequently used in platforms as it refers to a specific protocol. The aim of this task is to research and make sense to some of the various terminology. If you don't manage to get this working we'll still want to hear about what you tried, what worked and what didn't work, etc, as knowledge isn't required, just the ability to try figure things out! Good luck!

---

> ANSWER BOX
```
First, I pulled the matrixdotorg/synapse image from Docker Hub using the docker pull command. After that, I ran the server. To register as a user on this server, I used the docker exec -it command. Since Matrix Federation requires the HTTPS protocol, I set up Nginx to handle the encryption. Once the setup was complete, I tested the server using Matrix Federation Tester. Finally, I was able to send a message to @chino:oxn.sh.
```
