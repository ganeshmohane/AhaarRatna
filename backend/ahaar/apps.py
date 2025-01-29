import os
import pickle
from django.apps import AppConfig

class AhaarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ahaar'

    # Load pickle files on app startup
    def ready(self):
        pkl_dir = os.path.join(os.path.dirname(__file__), 'pkl_files')
        self.vectorizer = pickle.load(open(os.path.join(pkl_dir, 'vectorizer.pkl'), 'rb'))
        self.similarity = pickle.load(open(os.path.join(pkl_dir, 'similarity.pkl'), 'rb'))
        self.data = pickle.load(open(os.path.join(pkl_dir, 'data.pkl'), 'rb'))
