set -euo pipefail
echo "Starting core-dev tmux session"
echo "User: $(whoami), executing as regular user"

sudo -i -u turtle bash -c "echo $(whoami); tmux new-session -d -s 'core-dev' 'cd /Users/turtle/projects/tools/core-dev/core && source /Users/turtle/.zshrc && conda activate core-env && python3 main.py'"

echo "✓ Done"