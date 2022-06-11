import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import yaml
from scipy.spatial.distance import cosine
from src.utils.all_utils import read_yaml
import logging
import os
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'input_log.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


def retrieveEmbeddings(path_to_config, path_to_params, average_embeddings):
    config_path = read_yaml(path_to_config)
    param_path = read_yaml(path_to_params)
    index = param_path['index']
    logging.info(">>>> Serching embeddings .......")
    data = pickle.loads(open("faceEmbeddingModels/embeddings.pickle", "rb").read())
    distance=[]
    for i in range(index):
        embeddings = np.array(data['embeddings'+str(i)])
        average_embeddings = np.array(average_embeddings)
        distance.append(cosine(average_embeddings, embeddings))
    min = distance[0]
    minindex=0
    for j in range(len(distance)):
        if distance[j] < min:
            minindex = j
            min = distance[j]
    if min < 0.30:
        names = np.array(data['names' + str(minindex)])
        return names[0]
    else:
        return "none"






