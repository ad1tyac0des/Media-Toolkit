import os
import sys
import argparse
from PIL import Image
from colorama import init, Fore
import re
import subprocess
from tqdm import tqdm
from fontTools.ttLib import TTFont

# Initialize colorama
init(autoreset=True)


def print_info(message):
    print(f"\n{Fore.CYAN}{message}")


def print_success(message):
    print(f"\n{Fore.GREEN}{message}")


def print_error(message):
    print(f"\n{Fore.RED}{message}")


def print_warning(message):
    print(f"\n{Fore.YELLOW}{message}")


def convert_image(input_path, output_path, compression_level=0):
    with Image.open(input_path) as img:
        if compression_level > 0:
            quality = max(1, 100 - compression_level)
            img.save(output_path, quality=quality, optimize=True)
        else:
            img.save(output_path)


def get_video_duration(input_path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


def convert_video(input_path, output_path, compression_level=0):
    try:
        duration = get_video_duration(input_path)

        crf_value = min(
            51, 23 + (compression_level // 4)
        )  # Adjust CRF based on compression level

        process = subprocess.Popen(
            [
                "ffmpeg",
                "-i",
                input_path,
                "-c:v",
                "libvpx-vp9",
                "-crf",
                str(crf_value),
                "-b:v",
                "0",
                "-b:a",
                "128k",
                "-c:a",
                "libopus",
                output_path,
            ],
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        with tqdm(total=100, desc="Converting", unit="%", ncols=70) as pbar:
            for line in process.stderr:
                time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                if time_match:
                    hours, minutes, seconds = map(float, time_match.groups())
                    elapsed_time = hours * 3600 + minutes * 60 + seconds
                    progress = min(int(elapsed_time / duration * 100), 100)
                    pbar.update(progress - pbar.n)
                    pbar.refresh()

        process.wait()

        if process.returncode != 0:
            raise Exception(
                f"ffmpeg process failed with return code: {process.returncode}"
            )

    except Exception as e:
        print_error(f"Error during video conversion: {str(e)}")
        raise


def get_media_files(folder):
    image_files = []
    video_files = []
    for filename in os.listdir(folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            image_files.append(filename)
        elif filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_files.append(filename)
    return image_files, video_files


def convert_font(input_path, output_path, output_format):
    try:
        # Read input font
        font = TTFont(input_path)

        # Convert to desired format
        if output_format.lower() in ["ttf", "otf"]:
            # For TTF and OTF, we need to remove the WOFF/WOFF2 specific tables
            for table in ["WOFF", "wOFF", "WOFF2", "wOFF2"]:
                if table in font:
                    del font[table]
            # Set the flavor to None for TTF/OTF
            font.flavor = None
        elif output_format.lower() in ["woff", "woff2"]:
            # For WOFF and WOFF2, we set the appropriate flavor
            font.flavor = output_format.lower()
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Save converted font
        font.save(output_path)
        print_success(
            f"Successfully converted {os.path.basename(input_path)} to {os.path.basename(output_path)}"
        )
    except Exception as e:
        print_error(f"Failed to convert {os.path.basename(input_path)}: {str(e)}")


def get_font_files(folder):
    return [
        f
        for f in os.listdir(folder)
        if f.lower().endswith((".ttf", ".otf", ".woff", ".woff2"))
    ]


def main():
    parser = argparse.ArgumentParser(description="Media Converter")
    parser.add_argument("-conv", action="store_true", help="Convert files")
    parser.add_argument("-r", action="store_true", help="Rename files")
    parser.add_argument("-comp", action="store_true", help="Compress files")
    parser.add_argument(
        "-A", "--all", action="store_true", help="Perform all above operations"
    )
    parser.add_argument("-font", action="store_true", help="Convert font files")
    args = parser.parse_args()

    if args.font:
        if args.r or args.comp or args.all:
            print_warning(
                "Rename and compression options are not applicable for font conversion. These options will be ignored."
            )

        # Font conversion
        input_folder = input("Enter Folder Path: ").strip()
        if not os.path.isdir(input_folder):
            print_error("Invalid Folder Path.")
            sys.exit(1)

        print_info("Analyzing Folder Contents...")
        font_files = get_font_files(input_folder)
        if not font_files:
            print_warning("No Supported Font Files Found")
            sys.exit(1)

        output_folder = os.path.join(os.path.dirname(input_folder + "\\"), "converted_fonts")
        os.makedirs(output_folder, exist_ok=True)
        print_info(f"Created Output Folder: {output_folder}")

        font_format = (
            input(
                "Enter the desired font format (ttf, otf, woff, woff2, default is woff2): "
            )
            .strip()
            .lower()
            or "woff2"
        )
        if font_format not in ["ttf", "otf", "woff", "woff2"]:
            print_error(f"Unsupported font format: {font_format}")
            sys.exit(1)
        elif font_format == "woff2":
            print("Defaulting to woff2")

        for font_file in font_files:
            input_path = os.path.join(input_folder, font_file)
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(font_file)[0]}.{font_format}"
            )
            convert_font(input_path, output_path, font_format)
        print_success("Font Conversion Completed.")
        return

        # image and video processing
    if not (args.conv or args.r or args.comp or args.all):
        print_error(
            "Please specify at least one operation (-conv, -r, -comp, -A, or -font)"
        )
        sys.exit(1)

    input_folder = input("Enter the input folder path: ").strip()
    print(input_folder)
    if not os.path.isdir(input_folder):
        print_error("Invalid Folder Path.")
        sys.exit(1)

    print_info("Analyzing Folder Contents...")
    image_files, video_files = get_media_files(input_folder)

    if not (image_files or video_files):
        print_warning("No Supported Media Files Found")
        sys.exit(1)

    output_folder = os.path.join(os.path.dirname(input_folder + "\\"), "converted_media")
    os.makedirs(output_folder, exist_ok=True)
    print_info(f"Created Output Folder: {output_folder}")

    image_format = "webp"
    video_format = "webm"
    if args.conv or args.all:
        if image_files:
            image_format = (
                input("Enter the desired image format (default is webp): ").strip()
                or "webp"
            )
        if video_files:
            video_format = (
                input("Enter the desired video format (default is webm): ").strip()
                or "webm"
            )

    compression_level = 0
    if args.comp or args.all:
        compression_level = int(
            input("Enter compression level (0-100, 0 for no compression): ")
        )
        compression_level = max(0, min(100, compression_level))

    img_prefix = "img"
    vid_prefix = "vid"
    if args.r or args.all:
        if image_files:
            img_prefix = (
                input("Enter Prefix for Images (default is 'img'): ").strip() or "img"
            )
        if video_files:
            vid_prefix = (
                input("Enter Prefix for Videos (default is 'vid'): ").strip() or "vid"
            )

    total_files = len(image_files) + len(video_files)
    processed_files = 0

    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_folder, filename)
        if args.r or args.all:
            new_name = f"{img_prefix}{i}.{image_format}"
        else:
            new_name = f"{os.path.splitext(filename)[0]}.{image_format}"
        output_path = os.path.join(output_folder, new_name)
        try:
            print_info(f"Processing {filename} to {new_name}...")
            convert_image(input_path, output_path, compression_level)
            print_success(f"Successfully processed {filename} to {new_name}")
        except Exception as e:
            print_error(f"Failed to process {filename}: {str(e)}")

        processed_files += 1
        print_info(f"Overall Progress: {processed_files}/{total_files} files processed")

    for i, filename in enumerate(video_files, 1):
        input_path = os.path.join(input_folder, filename)
        if args.r or args.all:
            new_name = f"{vid_prefix}{i}.{video_format}"
        else:
            new_name = f"{os.path.splitext(filename)[0]}.{video_format}"
        output_path = os.path.join(output_folder, new_name)
        try:
            print_info(f"Processing {filename} to {new_name}...")
            convert_video(input_path, output_path, compression_level)
            print_success(f"Successfully processed {filename} to {new_name}")
        except Exception as e:
            print_error(f"Failed to process {filename}: {str(e)}")

        processed_files += 1
        print_info(f"Overall Progress: {processed_files}/{total_files} files processed")

    print_success("Processing Completed.")


if __name__ == "__main__":
    main()