import pickle
import yaml
from src.utils.all_utils import read_yaml
import logging
import os
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'input_log.log'), level=logging.INFO, format=logging_str,
                    filemode="a")

def storeEmbeddings(param_path, knownNames, average_embeddings):
    logging.info(">>>> Store embedding")
    # es.indices.create(index= config_path['index_name'], body=mapping)
    logging.info("Index created >>>")
    index = param_path['index']
    if index > 0:
        old_data = pickle.loads(open("faceEmbeddingModels/embeddings.pickle", "rb").read())
        old_data["embeddings" + str(index)] = average_embeddings
        old_data["names" + str(index)] = knownNames
        f = open("faceEmbeddingModels/embeddings.pickle", "wb")
        f.write(pickle.dumps(old_data))
        f.close()
        print(old_data)
    else:
        dict = {"embeddings" + str(index): average_embeddings, "names" + str(index): knownNames}
        f = open("faceEmbeddingModels/embeddings.pickle", "wb")
        f.write(pickle.dumps(dict))
        f.close()

    print("============================")
    index = index + 1
    dict = {'index':index}
    with open('../params.yaml', 'w') as yaml_file:
        yaml.dump(dict,yaml_file)
        yaml_file.close()
