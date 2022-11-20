# weather_bot
[@tesekkur_bot](http://t.me/tesekkur_bot)

How to run:

- install *docker and docker-compose* [somehow](https://docs.docker.com/compose/install/)
- [clone](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) this repo 
- change *path* and *HERE_YOUR_TELEGRAM_ID* in bot/docker-compose.yml
- add TOKEN from @BotFather to volumes/config_folder/config.py
- run `sudo docker-compose up --build` from **weather_bot/bot/** folder terminal
