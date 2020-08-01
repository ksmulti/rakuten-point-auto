import json

def LoadSettings():
  with open('settings.json', encoding='utf-8') as json_file:
    settings = json.load(json_file)
    return settings

def Login():
  print("Hello from a function")