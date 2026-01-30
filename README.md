# TODO
- Add more logging
- Make ctx and config as Response properties
- Clean codes 


# Dev
## Install Red Discord Bot
0. [Create Discord Bot and add to server](https://discord.com/developers/docs/quick-start/overview-of-apps) and get [Bot Token](https://discord.com/developers/docs/tutorials/developing-a-user-installable-app#fetching-app-credentials)
1. Run:
    ```sh
    git clone https://github.com/vcth4nh/vcth4nh-cogs.git
    cd vcth4nh-cogs
    uv sync
    source .venv/bin/activate
    redbot-setup --instance-name dev_cog2 --backend json --data-path ./dev_cog2 --no-prompt
    redbot dev_cog2 --dev --token <BOT TOKEN> --prefix '!'
    ```
2. Test Bot response:
    ```
    !help
    ```
3. Profit

## Install cog
1. Run
   ```
   uv pip install -r <cog name>/pyproject.toml
2. Go to Discord andAdd cog path:
    ```
    !addpath <path to this repo>/
    !load <cog name>
    ```

Read more [here](https://docs.discord.red/en/stable/guide_cog_creation.html#testing-your-cog)