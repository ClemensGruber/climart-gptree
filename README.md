# kiezbot
Our little Kiezbot for Berlin.
The Kiezbot is an converdsational AI box simulating three difference characters. It's made to interact with the citizens of Berlin to explain them "AI" in a playfull way.

We use a Python script to send a voice recording of user to mulipler Artificial Intelligence (AI) APIs:
- [Whisper AI](https://openai.com/research/whisper) for speech-to-text
- [ChatGPT 3.5](https://platform.openai.com/docs/models/gpt-3-5) as LLM that generates an answer

## Setup Environment
To install the requirements (globally) run:
`pip install -r requirements.txt` to install missing requirements

Create a `.env` file and add your API Keys like this:

`OPENAI_API_KEY="your-key"`

That's it. You are ready to go.

## Data Flow and Services

![Data Flow and Services](./img/THE-robot.svg)


