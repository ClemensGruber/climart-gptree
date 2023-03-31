![](https://img.shields.io/badge/Built%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiestiftung%20Berlin-blue)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

# Kiezbot Berlin
Our little Kiezbot Berlin is a conversational AI robot simulating three different characters. It's made to interact with the citizens of Berlin to **explain AI** in a playfull way.

We use a Python script to send a voice recording of user to multiple Artificial Intelligence (AI) APIs:
- [Whisper AI](https://openai.com/research/whisper) for speech-to-text
- [ChatGPT 3.5](https://platform.openai.com/docs/models/gpt-3-5) as LLM that generates an answer
- [Google Text-To-Speech](https://cloud.google.com/text-to-speech) to let the answer sound like a real character

## Setup Environment
To install the requirements (globally) run:
`pip install -r requirements.txt` to install missing requirements

Create a `.env` file and add your API Keys like this:

`OPENAI_API_KEY="your-key"`

`ELEVENLABS_API_KEY="your-key"`

**Run:** `python main.py`

That's it!

## Data Flow and Services

![Data Flow and Services](./img/THE-robot.svg)


## Credits

<table>
  <tr>
    <td>
      Made by <a href="https://citylab-berlin.org/de/start/">
        <br />
        <br />
        <img width="200" src="https://citylab-berlin.org/wp-content/uploads/2021/05/citylab-logo.svg" />
      </a>
    </td>
    <td>
      A project by <a href="https://www.technologiestiftung-berlin.de/">
        <br />
        <br />
        <img width="150" src="https://citylab-berlin.org/wp-content/uploads/2021/05/tsb.svg" />
      </a>
    </td>
    <td>
      Supported by <a href="https://www.berlin.de/rbmskzl/">
        <br />
        <br />
        <img width="80" src="https://citylab-berlin.org/wp-content/uploads/2021/12/B_RBmin_Skzl_Logo_DE_V_PT_RGB-300x200.png" />
      </a>
    </td>
  </tr>
</table>




