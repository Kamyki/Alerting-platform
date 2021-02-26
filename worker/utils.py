

def ERROR(x):
    print("==== " + str(x))
    exit(1)

DEBUG = False

LOG = lambda x : print("==== " + str(x)) if DEBUG else True


FROM = "matinekbot@gmail.com"
FROM_PW = "IRIO2021"

def send_email(addr, token, dead_url):
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, FROM_PW)

    msg = f"Hey, admin! Your service {dead_url} is dead! Please fix it and confirm you saw this message!\n \
        run 'python3 admin_cancel_incident.py --url {dead_url} --token {token}' to resolve incident!"
    server.sendmail("HEALTH WIZARD", addr, msg)
    
    LOG(f"INFO: Email to '{addr}' sent successfully!")
