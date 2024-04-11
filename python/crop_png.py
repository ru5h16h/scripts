#!/usr/bin/env python3

import argparse
import logging
import os

from PIL import Image

IMG_EX = ("png", "jpeg", "jpg")


def parse_arguments():
  """Parses command-line arguments for image cropping.

  Returns:
    argparse.Namespace: An object containing parsed arguments.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--image_path",
      type=str,
      required=True,
      help="Path to the PNG image file.",
  )
  parser.add_argument(
      "--top_left_x",
      type=int,
      required=True,
      help="X-coordinate of the top-left corner of the crop area.",
  )
  parser.add_argument(
      "--top_left_y",
      type=int,
      required=True,
      help="Y-coordinate of the top-left corner of the crop area.",
  )
  parser.add_argument(
      "--width",
      type=int,
      required=True,
      help="Width of the crop area.",
  )
  parser.add_argument(
      "--height",
      type=int,
      required=True,
      help="Height of the crop area.",
  )
  parser.add_argument(
      "--output_path",
      type=str,
      required=True,
      help="Path to save the cropped image file.",
  )
  return parser.parse_args()


def crop_png(image_path, top_left_x, top_left_y, width, height, output_path):
  """Crops a PNG image with the given specifications and saves to a new file.

  Args:
    image_path (str): Path to the PNG image file.
    top_left_x (int): X-coordinate of the top-left corner of the crop area.
    top_left_y (int): Y-coordinate of the top-left corner of the crop area.
    width (int): Width of the crop area.
    height (int): Height of the crop area.
    output_path (str): Path to save the cropped image file.
  """
  img = Image.open(image_path)
  crop_area = (top_left_x, top_left_y, top_left_x + width, top_left_y + height)
  cropped_img = img.crop(crop_area)
  cropped_img.save(output_path)


def main():
  args = parse_arguments()

  file_paths = []
  out_paths = []
  if os.path.isdir(args.image_path):
    for file_name in os.listdir(args.image_path):
      if file_name.endswith(IMG_EX):
        file_paths.append(os.path.join(args.image_path, file_name))
        out_paths.append(os.path.join(args.output_path, file_name))
    out_dir = args.output_path
  else:
    if args.image_path.endswith(IMG_EX) and args.output_path.endswith(IMG_EX):
      file_paths.append(args.image_path)
      out_paths.append(args.output_path)
    out_dir = os.path.dirname(args.output_path)

  if not file_paths:
    raise ValueError(f"No image file found.")
  os.makedirs(out_dir, exist_ok=True)

  for file_path, out_path in zip(file_paths, out_paths):
    logging.info(f"Cropping {file_path} to {out_path}.")
    crop_png(
        image_path=file_path,
        top_left_x=args.top_left_x,
        top_left_y=args.top_left_y,
        width=args.width,
        height=args.height,
        output_path=out_path,
    )


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  main()
