

def save_html(html: str):
    with open('output/response.html', 'w') as f:
        f.write(html)


def load_user_agents():
    with open('user_agents.txt', 'r') as f:
        ua = f.read()
    return ua.split('\n')


def load_proxies():
    with open('proxies.txt', 'r') as f:
        proxies = f.read()
    return proxies.split('\n')
