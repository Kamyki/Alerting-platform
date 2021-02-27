import os

def read_yaml(filename):
    import yaml
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            ERROR(exc)


SECRET_PATH = os.getenv("ALERTING_SECRET_PATH")

if SECRET_PATH is None:
    ERROR("ALERTING_SECRET_PATH env. variable not set! For docker please set it to '/app/secret.yaml', for host 'secret.yaml' or any other path you want")


SECRET_CONFIG = read_yaml(SECRET_PATH)
DEBUG = SECRET_CONFIG['debug']
DKRON_ADDRESS = SECRET_CONFIG['dkron_server']

if DEBUG:
    print("=== DEBUG variable set, output will be verbose...\n")


LOG = lambda x : print("==== " + str(x)) if DEBUG else True

def ERROR(x):
    print("==== " + str(x))
    exit(1)

FROM = "matinekbot@gmail.com"
FROM_PW = "IRIO2021"


def send_email(addr, token, dead_url):
    import yagmail
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, FROM_PW)

    api_endpoint = "http://127.0.0.1:5000/cancel (!! or another up-to-date address..)"

    msg = f"Hey, admin! Your service {dead_url} is dead! Please fix it and confirm you saw this message!\n \
        run 'python3 admin_cancel_incident.py --url {dead_url} --token {token} --endpoint {api_endpoint}' to resolve incident!"
    yag = yagmail.SMTP(FROM, FROM_PW)
    yag.send(addr, f"Your service is dead! {dead_url}", msg)
    LOG(msg)

    # server.sendmail("HEALTH WIZARD", addr, msg)

    LOG(f"INFO: Email to '{addr}' sent successfully!")
