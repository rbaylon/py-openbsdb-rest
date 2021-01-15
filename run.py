from openbsdrest import app

def main():
    print(" * ** Warning this is running in debug mode. For production deployment refer to https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#twisted-web .")
    app.run(host='0.0.0.0',port=app.config['LISTEN_PORT'],debug=True)

if __name__ == '__main__':
    main()
