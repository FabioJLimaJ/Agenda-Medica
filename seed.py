from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def criar_usuario():
    with app.app_context():
        
        db.create_all()
        admin = Usuario.query.filter_by(nome="admin").first()

        if not admin:
            senha_hash = generate_password_hash("senha123")

            novo_usuario = Usuario(
                nome="admin",
                email="admin@gmail.com",
                senha=senha_hash
            )

            db.session.add(novo_usuario)
            db.session.commit()
            print("usuario de teste cadastrado")
            print("Usuario : admin, Email: admin@gmail.com, senha: senha123")

        else:
            print("usuario de teste ja existente")

if __name__ == "__main__":
    criar_usuario()