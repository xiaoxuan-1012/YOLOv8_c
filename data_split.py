# -*- coding: utf-8 -*-
import os
import random
import shutil
from collections import Counter

SOURCE_ROOT = "dataset_org"
OUTPUT_ROOT = "dataset"

SPLIT_RATE = [0.8, 0.1, 0.1]
SPLIT_NAMES = ["train", "valid", "test"]

RANDOM_SEED = 42
SHUFFLE = True
PREFIX_FORMATION = True

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]


def get_label_path(label_root, formation, image_name):
    label_name = os.path.splitext(image_name)[0] + ".txt"

    path1 = os.path.join(label_root, formation, label_name)
    if os.path.exists(path1):
        return path1

    path2 = os.path.join(label_root, label_name)
    if os.path.exists(path2):
        return path2

    raise FileNotFoundError(
        "Label not found for image: {}\nTried:\n{}\n{}".format(
            image_name, path1, path2
        )
    )


def collect_samples():
    image_root = os.path.join(SOURCE_ROOT, "images")
    label_root = os.path.join(SOURCE_ROOT, "labels")

    if not os.path.isdir(image_root):
        raise FileNotFoundError("Missing folder: " + image_root)

    if not os.path.isdir(label_root):
        raise FileNotFoundError("Missing folder: " + label_root)

    formations = sorted(
        name for name in os.listdir(image_root)
        if os.path.isdir(os.path.join(image_root, name))
    )

    samples = []

    for formation in formations:
        folder = os.path.join(image_root, formation)

        for image_name in sorted(os.listdir(folder)):
            ext = os.path.splitext(image_name)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue

            image_path = os.path.join(folder, image_name)
            label_path = get_label_path(label_root, formation, image_name)

            samples.append({
                "formation": formation,
                "image_name": image_name,
                "image_path": image_path,
                "label_path": label_path
            })

    return samples


def split_samples(samples):
    samples = list(samples)

    if SHUFFLE:
        random.seed(RANDOM_SEED)
        random.shuffle(samples)

    total = len(samples)
    train_end = int(total * SPLIT_RATE[0])
    valid_end = int(total * (SPLIT_RATE[0] + SPLIT_RATE[1]))

    return {
        "train": samples[:train_end],
        "valid": samples[train_end:valid_end],
        "test": samples[valid_end:]
    }


def prepare_output():
    if os.path.exists(OUTPUT_ROOT):
        shutil.rmtree(OUTPUT_ROOT)

    for split_name in SPLIT_NAMES:
        os.makedirs(os.path.join(OUTPUT_ROOT, split_name, "images"))
        os.makedirs(os.path.join(OUTPUT_ROOT, split_name, "labels"))


def copy_data(split_data):
    for split_name, samples in split_data.items():
        image_out = os.path.join(OUTPUT_ROOT, split_name, "images")
        label_out = os.path.join(OUTPUT_ROOT, split_name, "labels")

        for sample in samples:
            formation = sample["formation"]
            image_name = sample["image_name"]

            if PREFIX_FORMATION:
                new_image_name = formation + "__" + image_name
                new_label_name = formation + "__" + os.path.splitext(image_name)[0] + ".txt"
            else:
                new_image_name = image_name
                new_label_name = os.path.splitext(image_name)[0] + ".txt"

            shutil.copy2(
                sample["image_path"],
                os.path.join(image_out, new_image_name)
            )

            shutil.copy2(
                sample["label_path"],
                os.path.join(label_out, new_label_name)
            )


def print_summary(split_data):
    total = sum(len(v) for v in split_data.values())

    print("\nDataset split completed")
    print("Train : Valid : Test = 8 : 1 : 1")
    print("Random seed =", RANDOM_SEED)
    print("-" * 50)

    for split_name in SPLIT_NAMES:
        samples = split_data[split_name]
        count_by_formation = Counter(
            sample["formation"] for sample in samples
        )

        print(
            "{}: {} images ({:.1f}%)".format(
                split_name,
                len(samples),
                len(samples) / total * 100
            )
        )

        for formation, count in sorted(count_by_formation.items()):
            print("   {}: {}".format(formation, count))

    print("-" * 50)
    print("Total images:", total)


def main():
    if abs(sum(SPLIT_RATE) - 1.0) > 1e-8:
        raise ValueError("SPLIT_RATE must sum to 1.0")

    samples = collect_samples()

    if not samples:
        raise RuntimeError("No images found in dataset_org/images")

    print("Found {} images".format(len(samples)))
    print("Formations:", sorted(set(x["formation"] for x in samples)))

    split_data = split_samples(samples)

    prepare_output()
    copy_data(split_data)
    print_summary(split_data)


if __name__ == "__main__":
    main()
