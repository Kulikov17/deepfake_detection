import torch
import cv2
import numpy as np
import pickle
from torch.autograd import Variable
from torchvision import transforms
from keras.preprocessing.image import img_to_array
from PIL import Image
from sklearn.linear_model import LogisticRegression

from models.mesonet import Meso4
from models.capsnet import CapsuleNet, VggExtractor

FILENAME_MESONET_WEIGHTS = './weights/Meso4_F2F.h5'
FILENAME_CAPSNET_WEIGHTS = './weights/capsnet_weights.pt'
FILENAME_ENSEMBLE_WEIGHTS = './weights/ensemble_model.pkl'

IMGSIZE = 256

class DeepfakeDetector:
  def __init__(self):
    self.gpu_id = -1 # cpu

    self.weak_learners = [
      ('meso4', Meso4()),
      ('capsnet', CapsuleNet(2, self.gpu_id)),
    ]

    self.model_load_weghts()


  def model_load_weghts(self):
    for clf_id, clf in self.weak_learners:
      if clf_id == 'meso4':
        clf.load(FILENAME_MESONET_WEIGHTS)
      if clf_id == 'capsnet':
        clf.load_state_dict(torch.load(FILENAME_CAPSNET_WEIGHTS, map_location='cpu'))

  def preprocessing_image(self, clf_id, img):
    if clf_id == 'meso4':
      img_ = cv2.resize(img, dsize=(IMGSIZE, IMGSIZE))
      img_ = img_ / 255
      img_array = img_to_array(img_)

      return np.expand_dims(img_array, axis=0)

    if clf_id == 'capsnet':
      img_pil = Image.fromarray(img).convert('RGB')
      img_data = transforms.Compose([
        transforms.Resize((IMGSIZE, IMGSIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
          mean=[0.485, 0.456, 0.406],
          std=[0.229, 0.224, 0.225]
        )
      ])(img_pil)

      return img_data.unsqueeze(0)

  def predict(self, img):
    weak_learners_predictions = []
    for clf_id, clf in self.weak_learners:
      if clf_id == 'meso4':
        img_data = self.preprocessing_image(clf_id, img)
        weak_learners_predictions.extend(clf.predict(img_data).tolist()[0])
      if clf_id == 'capsnet':
        img_data = self.preprocessing_image(clf_id, img)
        clf.eval()
        vgg_ext = VggExtractor()
        input_v = Variable(img_data)
        artifacts = vgg_ext(input_v)
        classes, class_ = clf(artifacts, random=True)
        output_dis = class_.data.cpu()
        prob = torch.softmax(output_dis, dim=1)[:, 1].data.numpy()
        weak_learners_predictions.extend(prob)

    with open(FILENAME_ENSEMBLE_WEIGHTS, 'rb') as ensemble_file:
      ensemble_model = pickle.load(ensemble_file)
      p = ensemble_model.predict([weak_learners_predictions])
      
    #prediction = np.mean(weak_learners_predictions)

    return p

