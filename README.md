# Setup

# Running the app 
1. Create a venv
```python3 -m venv env```
2. Activate env
```source env/bin/activate```
3. Install requirements
```pip install -r requirements.txt```
4. Get the secrets from Authenticator App, save as ```secrets.toml``` in ``.streamlit`` directory
4. Run the app
```streamlit run Tour_Results.py```

# To run against the test db
1. Change all refrences to of `textkey` to `textkeytest`