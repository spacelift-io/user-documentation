import requests

def on_config(config):
    wp_options_api_url = config['extra']['wp_options_api_url']

    if(wp_options_api_url):
        response = requests.get(wp_options_api_url)
        data = response.json()
        banner = data['acf']['docs_banner']
        config['extra'].update({'banner': banner})

    return config
