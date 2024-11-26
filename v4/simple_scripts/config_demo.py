from  aiomql import Config

# Initialize Config (looks for aiomql.json in the current directory or upwards)
config = Config()

# Access loaded attributes
print(config.login)  # Account login number
print(config.server, config.root)

# Dynamically Update Configuration
config.set_attributes(login=12345678, password="securepassword", server="MyBroker-Demo")
print(config.account_info())  # Output: {'login': 12345678, 'password': 'securepassword', 'server': 'MyBroker-Demo'}

# Custom Configuration File and Root

# Initialize with custom config file and project root
config = Config(root="../", filename='demo.json')

# Access global attributes
print(config.password, config.filename)  # Account password
print(config.records_dir)  # Path to trade records directory
