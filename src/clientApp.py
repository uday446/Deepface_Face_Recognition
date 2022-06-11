import argparse
import logging
import os
## Imports 
from face_embeddings.generate_embeddings import FaceEmbeddings
from face_predictor.generate_prediction import FacePredictor


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'input_log.log'), level=logging.INFO, format=logging_str,
                    filemode="a")

def getFaceEmbeddings():
    """
    Function to get the face embeddings from the images in the given directory
    """
    parser = argparse.ArgumentParser(description='Generate face embeddings')
    parser.add_argument('--faces', default= 50, help='Number of faces that the camera will get')
    parser.add_argument('--detector_backend', type=str, default='mtcnn', help='Face detector to be used')
    parser.add_argument('--config', default='config/config.yaml', help='Path to the config file', type=str)
    parser.add_argument('--params', default='../params.yaml', help='Path to the config file', type=str)

    args = vars(parser.parse_args())

    embeddings = FaceEmbeddings(args)
    embeddings.GenerateFaceEmbedding()
    return "success"


def getFacePrediction():
    """
    Function to get the face embeddings from the images in the given directory
    """
    parser = argparse.ArgumentParser(description='Generate face embeddings')
    parser.add_argument('--faces', default= 50, help='Number of faces that the camera will get')
    parser.add_argument('--detector_backend', type=str, default='mtcnn', help='Face detector to be used')
    parser.add_argument('--config', default='config/config.yaml', help='Path to the config file', type=str)
    parser.add_argument('--params', default='../params.yaml', help='Path to the config file', type=str)

    args = vars(parser.parse_args())

    embeddings = FacePredictor(args)
    embeddings.GenerateFacePrediction()
