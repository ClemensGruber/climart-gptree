# GPTree, a talking tree
## Data Flow and Services
We use a Python script to send a voice recording of user to multiple AI APIs:
- [Whisper](https://openai.com/research/whisper) for speech-to-text
- [ChatGPT 3.5](https://platform.openai.com/docs/models/gpt-3-5) as LLM that generates an answer
- [Google Cloud text-to-speech service](https://cloud.google.com/text-to-speech) to let the answer sound like a real character
![Data Flow and Services](./img/workflow-gptree.png)

## Credits
Danke an das CityLab Berlin! 
- Projekt [Kiezbot](https://citylab-berlin.org/de/exhibition/kiezbot/)
- Initialer code: https://github.com/technologiestiftung/kiezbot

<table>
    <td>
      Im Rahmen des ClimArt-Projekts von
      <br/>
    </td>
    <td>
      Initialer code vom 
      <br/>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://www.zku-berlin.org/de/">
        <img width="50" src="./img/zku-logo.png" />
      </a>
    </td>
    <td>
      <a href="https://citylab-berlin.org/de/start/">
        <img width="200" src="https://citylab-berlin.org/wp-content/uploads/2021/05/citylab-logo.svg" />
      </a>
    </td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
