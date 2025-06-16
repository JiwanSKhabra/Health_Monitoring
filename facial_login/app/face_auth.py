class FaceAuth:

    #
    def __init__(self, db_path = 'pass'):
        self.db_path = db_path


    # load images, compare using deepface or custom
    def verify_face(self, img1, img2):
        pass

    #extract embedding and store in file/DB
    def save_face(self, user_id, image):
        pass

    # load save embedding
    def load_face(self, user_id):
        pass

    # cosine similarity or euclidean distance
    def compare_embedding(self, emb1, emb2):
        pass


face_auth = FaceAuth()

output = face_auth.verify_face('blah', 'blah')
print(output)