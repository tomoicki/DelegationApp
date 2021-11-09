from app.create_flask_app import create_app
run = create_app()

if __name__ == '__main__':

    run.run(debug=False)
    # app.run(debug=False, host='0.0.0.0', port='19580')
