from app.app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
    # app.run(debug=False, host='192.168.224.1')
