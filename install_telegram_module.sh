project_name="TelegramChatbot"
# Clone project
git clone https://github.com/nlp4everyone/$project_name.git

# Delete modules
rm -rf telegram_modules
rm -rf config/telegram_params.py

# Check project
if [ ! -d "config" ]; then
   mkdir "config"
fi

# Copy module
cp -rf $project_name/telegram_modules telegram_modules
cp -rf $project_name/config/telegram_params.py config/telegram_params.py

# Remove whole project
rm -rf $project_name