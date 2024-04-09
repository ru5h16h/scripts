#!/usr/bin/env python3

import io
import logging
import os
import tarfile
import tqdm

import requests
from PIL import Image

CIFAR10_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
OUT_DIR = "cifar10"


def unpickle(file):
  import pickle
  with open(file, 'rb') as fo:
    dict_ = pickle.load(fo, encoding='bytes')
  return dict_


def extract_tar(file_obj):
  with tarfile.open(fileobj=file_obj, mode="r:gz") as tar:
    tar.extractall()
    extracted_files = tar.getnames()
  return extracted_files[0]


def save_images(batch_path, out_dir):
  data = unpickle(batch_path)
  img_data = data[b"data"]
  img_data = img_data.reshape((len(img_data), 3, 32, 32)).transpose(0, 2, 3, 1)
  file_names = data[b"filenames"]
  for idx, file_name in tqdm.tqdm(enumerate(file_names),
                                  ncols=79,
                                  total=len(file_names)):
    out_path = os.path.join(out_dir, file_name.decode('utf-8'))
    Image.fromarray(img_data[idx]).save(out_path)


def main():
  logging.info(f"Downloading CIFAR10 from {CIFAR10_URL} .")
  content = requests.get(CIFAR10_URL, stream=True).content

  logging.info(f"Extracting data.")
  content_bytes = io.BytesIO(content)
  extracted_dir = extract_tar(file_obj=content_bytes)

  for filename in os.listdir(extracted_dir):
    if filename.startswith("data"):
      out_dir = f"{OUT_DIR}/train"
      logging.info(f"Storing {filename} to {out_dir}")
      os.makedirs(out_dir, exist_ok=True)
      batch_path = os.path.join(extracted_dir, filename)
      save_images(batch_path, out_dir)

    if filename.startswith("test"):
      out_dir = f"{OUT_DIR}/test"
      logging.info(f"Storing {filename} to {out_dir}")
      os.makedirs(out_dir, exist_ok=True)
      batch_path = os.path.join(extracted_dir, filename)
      save_images(batch_path, out_dir)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  main()
