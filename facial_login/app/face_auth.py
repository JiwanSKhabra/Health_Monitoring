import os
import psycopg2
from deepface import DeepFace

class FaceAuth:

    def __init__(self, dbname='health_monitoring', user='postgres', host='127.0.0.1', port='5432'):
        self.db_config = {
            'dbname': dbname,
            'user': user,
            'password': os.getenv('PG_PASSWORD'),
            'host': host,
            'port': port
        }

    def verify_face(self, img1, img2):
        output = DeepFace.verify(img1, img2)
        return output

    def save_face(self, user_id, image):
        # Step 1: Extract embedding
        embedding = DeepFace.represent(img_path=image, model_name="Facenet")[0]['embedding']

        # Step 2: Format for PostgreSQL
        vector_str = '[' + ','.join(map(str, embedding)) + ']'

        # Step 3: Connect using config from __init__s
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        # Step 4: Insert into DB
        cur.execute(
            "INSERT INTO face_embeddings (name, embedding) VALUES (%s, %s);",
            (user_id, vector_str)
        )

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Saved face embedding for {user_id}")


    # load save embedding
    def load_face(self, user_id):
        pass

    # cosine similarity or euclidean distance
    def compare_embedding(self, emb1, emb2):
        pass


face_auth = FaceAuth()

face_auth.save_face("user001", "data/img1.jpg")
