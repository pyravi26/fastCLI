#!/usr/bin/env bash

PYTHON_VERSION=$(python3 --version)
VERSION_NUM=$(grep -Eo '\d.+' <<<$PYTHON_VERSION)

MAJOR=$(cut -d '.' -f 1 <<< "$VERSION_NUM")
MINOR=$(cut -d '.' -f 2 <<< "$VERSION_NUM")

if [ $(($MAJOR)) -lt 3 ] || ([ $(($MAJOR)) -eq 3 ] && [ $(($MINOR)) -lt 8 ]); then
    echo "Please use Python version 3.8 or higher"
    exit
fi

# SHELL_FILE=""
# _SHELL=$(grep -E '(zsh)$' <<<$0)
# echo $-2
# if [[ "$_SHELL" != "" ]]; then SHELL_FILE="$HOME/.zshrc"; fi

# if [[ "$SHELL_FILE" == "" ]]; then
#     _SHELL=$(grep -Eo 'bash' <<<$0)
#     if [[ "$_SHELL" != "" ]]; then SHELL_FILE="$HOME/.bashrc"; fi
# fi

# echo $SHELL_FILE

cp -r temp templates
python3 -m venv .environment && source .environment/bin/activate && pip install -r requirements.txt && python ./fastcli.py --
echo " " >> ~/.zshrc
echo " " >> ~/.zshrc
echo "# Set Executable FastCLI" >> ~/.zshrc

C_PATH=$(pwd)

echo "#!/usr/bin/env bash" >> "$C_PATH/fastCLI.sh"
echo "SOURCE_PATH=\$(pwd)" >> "$C_PATH/fastCLI.sh"
echo "cd $C_PATH && source .environment/bin/activate && python fastcli.py \$@ --source=\$SOURCE_PATH" >> "$C_PATH/fastCLI.sh"
CH_MOD=$(chmod +x $C_PATH/fastCLI.sh)

echo "alias fastCLI='sh $C_PATH/fastCLI.sh'" >> ~/.zshrc
source ~/.zshrc