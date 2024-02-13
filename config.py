from aiomql import Config, Account

config = Config()

# config contains some default values
print(config.filename)  # aiomql.json by default. but this file does not exist as yet.

# loading a config file from an instance of Config
# it looks for a file with the filename in the current directory
config.load_config(filename='config.json')

# specifying a config directory and filename during instantiation
# it looks for a file with the filename in the specified directory
# configs must be relative to the root directory
# specify reload=True to reload the config file. since this not the first time we are loading the config file
config = Config(config_dir='configs', filename='config.json', reload=True)

# update login and password details
Config(login=123456, password='password', server='server')

# get account details  as a dictionary
print(config.account_info())  # {'login': 123456, 'password': 'password', 'server': 'server'}

# access it from the account object
# All classes that inherits from the Base class have an instance of the Config class
account = Account()
print(account.config.login)
