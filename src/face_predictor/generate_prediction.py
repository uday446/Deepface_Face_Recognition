from src.deepface.deepface.detectors import FaceDetector
from src.deepface.deepface import DeepFace
from vidgear.gears import CamGear
import cv2
import os
import logging
import time
from src.utils.all_utils import print_exams_average, read_yaml
from datetime import datetime
from src.deepface.deepface.commons import functions
from src.face_simmilarity.retrieve_embeddings import retrieveEmbeddings

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'input_log.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


class FacePredictor:

    def __init__(self, args):
        self.args = args
        self.facedetector = FaceDetector
        self.deepface = DeepFace
        self.detector = 'mtcnn'

    def GenerateFacePrediction(self):
        config_path = read_yaml(self.args['config'])
        face_detector = self.facedetector.build_model(self.args['detector_backend'])
        cap = CamGear(source=0, logging=True).start()
        #cap = cv2.VideoCapture(0)
        faces1= 0
        frames = 0
        max_faces = int(self.args["faces"])

        model = self.deepface.build_model("Facenet")
        while faces1 < max_faces:
            frame = cap.read()
            frames += 1
            if frames % 1 == 0:
                faces = FaceDetector.detect_faces(face_detector, self.args['detector_backend'], frame, align=False)
                try:
                    img = functions.preprocess_face(frame, target_size= (model.input_shape[1], model.input_shape[2]), detector_backend= 'mtcnn', enforce_detection= False)
                    tic = time.time()
                    embedding = model.predict(img)[0].tolist()

                    print(embedding)
                    res = retrieveEmbeddings(self.args['config'], self.args['params'], embedding)
                    person = res

                    toc = time.time()
                    logging.info(f">>>>>>Time is : {toc - tic}<<<<<<<<")
                except Exception as e:
                    logging.exception(e)
                    continue

                for face, (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (67,67,67), 2)
                    cv2.putText(frame, person, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            #         print('Face detected')
                faces1 += 1
            cv2.imshow("Face detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        cap.stop()
