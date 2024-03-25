import toml

output_file = ".streamlit/secrets-test-2.toml"

with open("nzdg-tour-2023-063b3ba861de.json") as json_file:
    json_text = json_file.read()

config = {"textkey2": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)
