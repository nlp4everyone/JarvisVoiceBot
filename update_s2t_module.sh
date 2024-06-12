project_name="SpeechModule"
# Clone project
git clone https://github.com/nlp4everyone/$project_name.git

# Remove project
rm -rf speech2text_modules
rm -rf config/transcript_params.py

# Copy folder
cp -rf $project_name/speech2text_modules speech2text_modules
cp -rf $project_name/config/transcript_params.py config/transcript_params.py

# Install dependencies
pip install -r $project_name/requirements_intergrations.txt

# Remove whole project
rm -rf $project_name