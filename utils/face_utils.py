import os
import cv2
import face_recognition
import pickle
from config import Config

def train_model():
    """
    Reads images from the dataset directory, extracts face encodings,
    and saves them to a pickle file for later recognition.
    """
    known_face_encodings = []
    known_face_names = []
    
    dataset_dir = Config.DATASET_DIR
    
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(root, file)
                
                # The folder name is the student_id
                student_id = os.path.basename(root)
                
                # Load image and find face encodings
                image = face_recognition.load_image_file(path)
                
                # We assume only one face per image for dataset
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    encoding = encodings[0]
                    known_face_encodings.append(encoding)
                    known_face_names.append(student_id)
                    
    # Save the encodings
    data = {"encodings": known_face_encodings, "names": known_face_names}
    model_path = os.path.join(Config.MODELS_DIR, "encodings.pickle")
    
    with open(model_path, "wb") as f:
        pickle.dump(data, f)
        
    return True

def load_model():
    """
    Loads the trained model from the pickle file.
    """
    model_path = os.path.join(Config.MODELS_DIR, "encodings.pickle")
    if not os.path.exists(model_path):
        return None
        
    with open(model_path, "rb") as f:
        data = pickle.load(f)
    return data
