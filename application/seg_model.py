from flask import current_app as app
from torchvision import models
import torchvision.transforms as T

from PIL import Image
import torch
import numpy as np

from pathlib import PurePath


model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()


def Compose(size_t, min_size=512):
  new_size = min(size_t[0], size_t[1], min_size)
  return T.Compose([T.Resize(new_size),
                    T.ToTensor(),
                    T.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])])


def decode_segmap(image, nc=21):

    label_colors = np.array([(0, 0, 0),  # 0=background
                             # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                             (128, 0, 0), (0, 128, 0), (128, 128,
                                                        0), (0, 0, 128), (128, 0, 128),
                             # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                             (0, 128, 128), (128, 128, 128), (64,
                                                              0, 0), (192, 0, 0), (64, 128, 0),
                             # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                             (192, 128, 0), (64, 0, 128), (192, 0,
                                                           128), (64, 128, 128), (192, 128, 128),
                             # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                             (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]

    rgb = np.stack([r, g, b], axis=2)
    return rgb


def evaluate_image(image_path):
    path = PurePath(image_path)
    out = None
    with Image.open(image_path) as img:
        trf = Compose(img.size)
        inp = trf(img).unsqueeze(0)
        with torch.no_grad():
            out = model(inp)['out']
    om = torch.argmax(out.squeeze(), dim=0).detach().numpy()
    rgb = decode_segmap(om)
    out_img = Image.fromarray(rgb)
    out_path = path.stem + '_out.jpg'
    out_img.save(str(path.parent/out_path))
    return out_path
