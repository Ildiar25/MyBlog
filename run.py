from app import db, create_app
from app.public.models import Post
from app.auth.models import User


def main():
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == '__main__':
    main()
