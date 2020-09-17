from url_shortener import application, db


db.create_all()
app = application.run(host="0.0.0.0", port=int(application.config['PORT']),
                      debug=True)
