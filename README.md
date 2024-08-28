
# Telegram Editor Bot

A powerful tool to interact with videos and modify them that uses moviepy (FFMPEG) under the hood. It is able to crop, concat and speed videos up. All that with a telegram frontend, which makes it really easy to share the results with your friends.


## Run Locally

### Clone the project

```bash
  git clone https://github.com/NotisFobbidden/telegramEditorBot.git
```

### Go to the project directory

```bash
  cd telegramEditorBot
```

### Install dependencies
Install the python modules
```bash
  pip3 install -r requirements.txt
```
Install FFMPEG (Example for debian-based distos)
```bash
  sudo apt install ffmpeg
```

### Make a config.py file with the following constant

```bash
  TOKEN="yourBotsToken"
```

### Start the bot

```bash
  python3 main.py
```

### Enjoy
