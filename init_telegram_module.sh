project_name="TelethonChatbot"
# Clone project
git clone https://github.com/nlp4everyone/$project_name.git

# Delete modules
rm -rf component_samples
rm -rf config/telegram_params.py
rm -rf sample_bot_service.py

# Check project
if [ ! -d "config" ]; then
   mkdir "config"
fi

# Copy module
cp -rf $project_name/component_samples component_samples
cp -rf $project_name/config/telegram_params.py config/telegram_params.py
cp -rf $project_name/sample_bot_service.py sample_bot_service.py

# Remove whole project
rm -rf $project_name