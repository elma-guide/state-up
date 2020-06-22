import json
import sys

from json.decoder import JSONDecodeError
from requests import Session
from hashlib import sha1


def error(message):
    print(f'[ERROR] {message}')


def upload_state(username, password, state_path):
    '''
    Logs in to stats and uploads the state file.

    Returns whether the file was successfully uploaded.
    '''

    with Session() as session:
        url = 'http://stats.sshoyer.net/up.php'

        print('Logging you in')
        response = session.post(url, data={
            'nick': username,
            'pwd': password,
            'remembar': 'ye'
        })

        if response.status_code < 200 or response.status_code > 299:
            error(f'HTTP {response.status_code} not expected.')
            return False

        content = response.content.decode('utf8')
        if 'Wrong password!' in content:
            error('Password is incorrect')
            return False
        if "User doesn't exist!" in content:
            error('Account does not exist')
            return False

        print(f'Uploading {state_path}')
        response = session.post(
            url,
            data={'MAXFILESIZE': '3000000'},
            files={'uploadedfile': open(state_path, 'rb')}
        )

        content = response.content.decode('utf8')
        if 'Stats uploaded!' in content:
            print(f'{state_path} upload finished.')
            return True
        else:
            error(f'{state_path} upload failed.')
            return False


def write_config(config):
    '''
    Writes `config` to the default config file location.
    '''

    with open(config_file, 'w') as fp:
        json.dump(config, fp, indent=4)


def write_config_template():
    '''
    Writes the default config template to the default config file location.
    '''

    config = {
        'settings': {
            'username': 'enter_your_username_here',
            'password': 'enter_your_password_here',
            'state.dat': './state.dat'
        },
        'data': {
            'hash': ''
        }
    }

    write_config(config)


def load_config():
    '''
    Loads the config from the default config file location.

    Returns whether the config was successfully loaded.
    '''

    try:
        with open(config_file) as fp:
            return json.load(fp)
    except FileNotFoundError:
        print('Configuration file not found.')
        try:
            write_config_template()
        except OSError:
            error('Failed to write file.')
            return None
        print(
            f'Configuration file template saved to {config_file}.\nOpen it and save your username and password before running this script again.')
        return None
    except JSONDecodeError:
        error('Illegal json in configuration file.\nFix it or delete the file before running this script again.')
        return None


def state_hash(state_file):
    '''
    Returns the hash of the file located at `state_file`.
    '''

    with open(state_file, 'rb') as file:
        return sha1(file.read()).hexdigest()


config_file = 'stateup.config.json'


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--log':
        try:
            sys.stdout = open('stateup.log', 'w')
        except IOError:
            error('--log provided but could not open log file for writing.')
            exit(-1)

    config = load_config()
    
    if config is None:
        error("Failed to load config")
        exit(-1)

    try:
        username = config['settings']['username']
        password = config['settings']['password']
        state_path = config['settings']['state.dat']
    except KeyError:
        error('Invalid config. Delete it and generate a new one.')
        exit(-1)

    # Check if state file has changed
    previous_hash = config['data']['hash']
    try:
        hash = state_hash(state_path)
    except FileNotFoundError:
        error(f'{state_path} could not be hashed. Does it exist?')
        exit(-1)
    
    if hash == previous_hash:
        print(f'{state_path} has not changed. Nothing to do.')
        exit()

    if upload_state(username, password, state_path):
        # Save hash to check next time
        config['data']['hash'] = hash
        write_config(config)
        print('Done')
    else:
        exit(-1)
