import toml

output_file = ".streamlit/secrets-test.toml"

with open("nzdg-test-env-firebase-adminsdk-llxlt-1b785bd5a9.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)
