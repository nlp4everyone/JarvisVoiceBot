project_name="ChatModule"
# Clone project
git clone https://github.com/nlp4everyone/$project_name.git

# Remove project
rm -rf chat_modules
rm -rf config/params.py
rm -rf config/llama_index_config.json

# Copy folder
cp -rf $project_name/chat_modules chat_modules
cp -rf $project_name/config/params.py config/params.py
cp -rf $project_name/config/llama_index_config.json config/llama_index_config.json

# Remove whole project
rm -rf $project_name