import os
import numpy as np
import psycopg2
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity


class FaceAuth:

    def __init__(self):
        self.db_config = {
            'dbname': 'health_monitoring',
            'user': 'postgres',
            'password': os.getenv('PG_PASSWORD'),
            'host': '127.0.0.1',
            'port': 5432
            }

    def verify_face(self, img1, img2):
        try:
            output = DeepFace.verify(
                img1_path = img1,
                img2_path = img2,
                model_name="Facenet",
                detector_backend="opencv",
                enforce_detection=False
            )
            return output
        except Exception as e:
            print(f"[ERROR] Falied to verify face{e}")
            return None

    def save_face(self, user_id, image):
        try:
            # Extract embedding
            embedding = DeepFace.represent(
                img_path=image,
                model_name="Facenet",
                enforce_detection=False
            )[0]['embedding']

            # Format for PostgreSQL
            vector_str = '[' + ','.join(map(str, embedding)) + ']'

            # Connect and insert
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO face_embeddings (name, embedding) VALUES (%s, %s);",
                (user_id, vector_str)
            )

            conn.commit()
            print(f"✅ Saved face embedding for {user_id}")

        except Exception as e:
            print(f"[ERROR] Failed to save face embedding for {user_id}: {e}")

        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass


    # load save embedding
    def load_face(self, user_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()

            cur.execute("SELECT embedding FROM face_embeddings WHERE id = %s;", (user_id,))
            result = cur.fetchone()

            if not result:
                print(f"[WARN] No embedding found for user_id: {user_id}")
                return None

            embedding_str = result[0]
            embedding = np.array([float(x) for x in embedding_str.strip('[]').split(',')])
            return embedding
        except Exception as e:
            print(f"[ERROR] Failed to load embedding for user_id={user_id}: {e}")
            return None

        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    # cosine similarity or euclidean distance
    def compare_embedding(self, emb1, emb2):
        try:
            emb1 = np.array(emb1).reshape(1, -1)
            emb2 = np.array(emb2).reshape(1, -1)
            return cosine_similarity(emb1, emb2)[0][0]
        except Exception as e:
            print("[ERROR] Failed to compare embedding {e}")
            return None



face = FaceAuth()
face1 = face.load_face(1)
face2 = face.load_face(2)

print(face.compare_embedding(face1, face2))