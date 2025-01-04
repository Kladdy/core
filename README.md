# Core

## Start

```bash
tmux new-session -d -s 'core-dev' 'cd /Users/turtle/projects/tools/core-dev/core && source /Users/turtle/.zshrc && conda activate core-env && python3 main.py'
```

### Old

```bash
screen -S core
cd ~/projects/tools/core-dev/core && conda activate core-env && python3 main.py
```


sudo chown root /Users/turtle/projects/tools/core-dev/startcore.plist

sudo ln -s /Users/turtle/projects/tools/core-dev/startcore.plist /Library/LaunchAgents/startcore.plist 
sudo launchctl load /Library/LaunchAgents/startcore.plist 

## Commando in plist
tmux new-session -d -s 'core-dev' 'sleep 1; cd /Users/turtle/projects/tools/core-dev/core && source /Users/turtle/.zshrc && conda activate core-env && python3 main.py; sleep 1'