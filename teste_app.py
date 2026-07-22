import unittest
from app import app, db, Usuario
from werkzeug.security import generate_password_hash

class AgendaMedicaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        usuario_teste = Usuario(
            nome="admin",
            email="admin@gmail.com",
            senha=generate_password_hash("senha123")
        )
        db.session.add(usuario_teste)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post('/', data={
            'login_input': 'admin',
            'senha': 'senha123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_incorreto(self):
        response = self.client.post('/', data={
            'login_input': 'admin',
            'senha': 'senha321'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api(self):
        response = self.client.get('/api/agendamentos')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertIn('paciente', response.json[0])

if __name__ == '__main__':
    unittest.main()