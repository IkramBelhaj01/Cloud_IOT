from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes import auth
from redis import Redis
from redis.exceptions import ConnectionError

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation du client Redis avec gestion d'erreur
redis_client = None
try:
    redis_client = Redis.from_url(app.config["REDIS_URL"])  # Utilisation de l'URL de connexion Redis définie dans la config
    redis_client.ping()  # Vérifier la connexion à Redis
    print("Connexion Redis réussie")
except ConnectionError:
    print("Erreur de connexion à Redis. Vérifiez la configuration.")
    # redis_client reste None en cas d'erreur


jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    if redis_client is None:
        print("Redis client est non défini ou non connecté.")
        return False
    try:
        jti = jwt_payload["jti"]
        return redis_client.exists(jti)
    except Exception as e:
        print(f"Erreur lors de la vérification du token dans la blacklist Redis: {str(e)}")
        return False

# Enregistrer les routes
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
