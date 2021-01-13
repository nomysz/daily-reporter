## How to use?
Go ahead and change `config.py.dist` to `config.py` 
and fill with neccessary data. 

For JIRA create api token.

For Slack create app with permissions `chat:write` and `chat:write.customize` 
publish it to workspace.

For rephraser subscribe to Basic plan (free) of Deep Translate API 
in RapidAPI and configure `RAPIDAPI_API_KEY`.

Run as `python3 daily-reporter.py` after installing requirements.

## Todo
- remove username and icon from config and download it from Slack profile
- multiple rephraze to get more random status descriptions
- add chance to remove random word to get differently rephased sentence
- get JIRA comments to issue and mix it with description
- "forget" and post some issues as comments to original one
- get issue comments and report activity based on them
