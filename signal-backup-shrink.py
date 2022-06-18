#!/usr/bin/env python3

import argparse
import glob
import os
from shutil import which

import filetype
from PIL import Image


def tool_in_path(name: str) -> bool:
    return which(name) is not None


def is_match(string: str, *patterns: str) -> bool:
    return any(p in string for p in patterns)


def strip_file_ext(file: str) -> str:
    return os.path.basename(file).split(".")[0]


def newfile_path(file: str, ext: str = "new") -> str:
    filename = strip_file_ext(file)
    newfile = f"{filename}.{ext}"
    return f"{os.path.dirname(file)}/{newfile}"


def create_newfile_from_temp(file: str, tempfile: str) -> None:
    newfile = newfile_path(file)
    if os.path.exists(tempfile):
        os.replace(tempfile, newfile)


def guess_filetype(file: str) -> str:
    kind = filetype.guess(file)
    if kind is not None:
        return kind.extension
    else:
        return ""


def print_size_change(file: str, filetype: str, oldsize: int) -> None:
    newfile = newfile_path(file)
    if os.path.exists(newfile):
        newsize = int(os.path.getsize(newfile) / 1000)
    else:
        newsize = 0

    print(f"{filetype}: {oldsize}kB -> {newsize}kB ({os.path.basename(file)})")


def vid_to_collage(file: str, ext: str = "jpg", w: int = 500) -> None:
    tempfile = newfile_path(file, ext)
    os.system(
        f"vcsi {file} -g 2x2 -w {w} --metadata-position hidden -o {tempfile} > /dev/null 2>&1"
    )
    create_newfile_from_temp(file, tempfile)


def img_shrink(file: str, ext: str = "jpg", w: int = 500) -> None:
    im = Image.open(file)
    w_percent = w / float(im.size[0])
    h = int((float(im.size[1]) * float(w_percent)))

    im = im.resize((w, h), Image.Resampling.LANCZOS)
    tempfile = newfile_path(file, ext)
    im.save(tempfile)

    create_newfile_from_temp(file, tempfile)


def imgs_to_grid(imgs: list, rows: int = 2, cols: int = 2) -> Image.Image:
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


def gif_to_collage(
    file: str, num_frames: int = 4, thumb_size: tuple = (480, 360), ext: str = "jpg"
) -> None:
    im = Image.open(file)

    thumbnails = []
    for i in range(num_frames):
        im.seek(im.n_frames // num_frames * i)
        frame = im.copy()
        frame.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        thumbnails.append(frame)

    collage = imgs_to_grid(thumbnails)
    tempfile = newfile_path(file, ext)
    collage.save(tempfile)

    create_newfile_from_temp(file, tempfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("signal_backup_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.signal_backup_dir):
        exit("Backup directory not found")

    if not tool_in_path("vcsi"):
        exit("vcsi not found in PATH")

    for file in glob.glob(f"{args.signal_backup_dir}/Attachment*.bin"):
        filesize_kb = int(os.path.getsize(file) / 1000)
        if filesize_kb < 200:
            continue

        filetype = guess_filetype(file)
        if not filetype:
            continue

        if is_match(filetype, "jpg", "jpeg", "png"):
            img_shrink(file, filetype)
            print_size_change(file, filetype, filesize_kb)
        elif is_match(filetype, "mp4", "mkv", "3gp"):
            vid_to_collage(file)
            print_size_change(file, filetype, filesize_kb)
        elif is_match(filetype, "gif"):
            gif_to_collage(file)
            print_size_change(file, filetype, filesize_kb)


if __name__ == "__main__":
    main()
