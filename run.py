from app import AppConfig, db, create_app


def main():
    app = create_app(AppConfig.DEV)
    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == '__main__':
    main()
