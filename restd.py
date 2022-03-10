import jwt
import os
import datetime
import stat
from views import app

token = jwt.encode({'username' : 'admin',
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=365)},
        app.config['SECRET_KEY'])

home = os.environ['HOME']
with open(f"{home}/.restd.token", "w") as file:
    file.write(token)

os.chmod(f"{home}/.restd.token", stat.S_IRWXU)

def main():
    print(" * ** Warning this is running in debug mode. For production deployment refer to https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#twisted-web .")
    app.run(host='0.0.0.0',port=app.config['LISTEN_PORT'],debug=True)

if __name__ == '__main__':
    main()
