#!/usr/bin/env bash

echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
echo '         Start Process'
echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

PYTHON_VERSION=$(python3 --version)
VERSION_NUM=$(grep -Eo '\d.+' <<<$PYTHON_VERSION)

MAJOR=$(cut -d '.' -f 1 <<< "$VERSION_NUM")
MINOR=$(cut -d '.' -f 2 <<< "$VERSION_NUM")

if [ $(($MAJOR)) -lt 3 ] || ([ $(($MAJOR)) -eq 3 ] && [ $(($MINOR)) -lt 8 ]); then
    echo "Please use Python version 3.8 or higher"
    exit
fi

sudo cp -R $(pwd) /var/
sudo rm -rf /var/fast-cli/.git /var/fast-cli/.environment /var/fast-cli/.key /var/fast-cli/templates /var/fast-cli/fastCLI.sh /var/fast-cli/.gitignore

#$(pwd)
C_PATH=/var/fast-cli
SHELL_CONFIG_FILE="$HOME/.$(sed s/-// <<<$1)rc"

cp -r $C_PATH/temp $C_PATH/templates
cd $C_PATH && python3 -m venv .environment && source .environment/bin/activate && pip install -r requirements.txt && python ./fastcli.py --

echo -e "#!/usr/bin/env bash\nSOURCE_PATH=\$(pwd)\n" >> "$C_PATH/fastCLI.sh"
echo "cd $C_PATH && source .environment/bin/activate && python fastcli.py \$@ --source=\$SOURCE_PATH" >> "$C_PATH/fastCLI.sh"
chmod +x $C_PATH/fastCLI.sh

sudo ln -s $C_PATH/fastCLI.sh /usr/local/bin/fastCLI

# if grep -q -F "Set Executable FastCLI" "$SHELL_CONFIG_FILE"; then 
#     echo ""
# else
#     echo -e "\n\n# Set Executable FastCLI\nalias fastCLI='sh $C_PATH/fastCLI.sh'" >> $SHELL_CONFIG_FILE
#     source $SHELL_CONFIG_FILE
# fi