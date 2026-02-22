#!/usr/bin/env bash

echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
echo '         Start Process'
echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

PYTHON_VERSION=$(python3 --version)
# specific to macOS or Linux depending on grep version, using [0-9] is safer than \d
VERSION_NUM=$(grep -Eo '[0-9]+\.[0-9]+' <<<$PYTHON_VERSION)

MAJOR=$(cut -d '.' -f 1 <<< "$VERSION_NUM")
MINOR=$(cut -d '.' -f 2 <<< "$VERSION_NUM")

if [ $(($MAJOR)) -lt 3 ] || ([ $(($MAJOR)) -eq 3 ] && [ $(($MINOR)) -lt 8 ]); then
    echo "Please use Python version 3.8 or higher"
    exit 1
fi

# Check for venv module (common issue on Debian/Ubuntu)
if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Error: 'python3-venv' module not found."
    echo "On Debian/Ubuntu, please run: sudo apt-get install python3-venv"
    exit 1
fi

sudo cp -R $(pwd) /var/

# Remove existing files/dirs if they exist
for dir in ".git" ".key" "templates"; do
    if [ -d "/var/fast-cli/$dir" ]; then
        sudo rm -rf "/var/fast-cli/$dir"
    fi
done

for file in "fastCLI.sh" ".gitignore"; do
    if [ -f "/var/fast-cli/$file" ]; then
        sudo rm -rf "/var/fast-cli/$file"
    fi
done

#$(pwd)
C_PATH=/var/fast-cli

# Detect shell config file
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG_FILE="$HOME/.bashrc"
    else
        SHELL_CONFIG_FILE="$HOME/.bash_profile"
    fi
else
    # Fallback to the logic used before but safer
    SHELL_NAME=$(basename "$SHELL")
    SHELL_CONFIG_FILE="$HOME/.${SHELL_NAME}rc"
fi

sudo cp -r $C_PATH/temp $C_PATH/templates
sudo bash -c "cd $C_PATH && python3 -m venv .environment && source .environment/bin/activate && pip install -r requirements.txt && python ./fastcli.py --"

echo -e "#!/usr/bin/env bash\nSOURCE_PATH=\$(pwd)\n" | sudo tee "$C_PATH/fastCLI.sh" > /dev/null
echo "cd $C_PATH && source .environment/bin/activate && python fastcli.py \$@ --source=\$SOURCE_PATH" | sudo tee -a "$C_PATH/fastCLI.sh" > /dev/null
sudo chmod +x $C_PATH/fastCLI.sh

sudo ln -sf $C_PATH/fastCLI.sh /usr/local/bin/fastCLI

# if grep -q -F "Set Executable FastCLI" "$SHELL_CONFIG_FILE"; then 
#     echo ""
# else
#     echo -e "\n\n# Set Executable FastCLI\nalias fastCLI='sh $C_PATH/fastCLI.sh'" >> $SHELL_CONFIG_FILE
#     source $SHELL_CONFIG_FILE
# fi