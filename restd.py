import jwt
import os
import datetime
import stat
from views import app

token = jwt.encode({'username' : app.config['LOCAL_API_USER'],
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=365)},
        app.config['SECRET_KEY'])

home = os.environ['HOME']
if not os.path.isfile(f"{home}/.restd.token"):
    with open(f"{home}/.restd.token", "w") as file:
        file.write(token)

    os.chmod(f"{home}/.restd.token", stat.S_IRWXU)

def main():
    app.run(host='0.0.0.0',port=app.config['LISTEN_PORT'],debug=True)

if __name__ == '__main__':
    main()
