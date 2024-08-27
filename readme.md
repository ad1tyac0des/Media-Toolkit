# Media Toolkit

Media Toolkit is a powerful Python script designed for web development asset optimization/management. It helps prepare media files for efficient use in web projects by converting, compressing, and renaming various types of media assets.

## Purpose

The main purpose of this script is to streamline the process of optimizing media assets for web development. It automates several common tasks that developers often need to perform manually, saving time and ensuring consistency across projects.

## Features

- **Image Conversion**: Convert images to web-friendly formats (e.g., WebP)
- **Video Conversion**: Convert videos to web-optimized formats (e.g., WebM)
- **Font Conversion**: Convert fonts to desired formats (default: WOFF2)
- **Compression**: Reduce file sizes of images and videos to improve loading times
- **Batch Renaming**: Rename files in a consistent manner for easier management in WebDev
- **Progress Tracking**: Display progress bars and overall completion status
- **Flexible Output**: Customizable output formats and compression levels

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ad1tyac0des/Media-Toolkit.git
   cd Media-Toolkit
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have FFmpeg installed on your system for video processing and add it to your PATH:
   - Download FFmpeg for your operating system from: https://www.ffmpeg.org/download.html
   - Follow the installation instructions for your specific OS
   - Add FFmpeg to your system's PATH
   - For a detailed guide, consider watching a tutorial on YouTube about installing FFmpeg

## Usage

Run the script from the command line with the desired flags:

```
python MediaToolkit.py [options]
```

### Command-line Options

- `-conv`: Convert files to web-friendly formats
- `-r`: Rename files with consistent prefixes
- `-comp`: Compress files to reduce size
- `-A` or `--all`: Perform all above operations (convert, rename, and compress)
- `-font`: Convert font files

### Examples

1. Convert and compress all media files:
   ```
   python MediaToolkit.py -conv -comp
   ```

2. Convert font files:
   ```
   python MediaToolkit.py -font
   ```

3. Perform all operations on media files:
   ```
   python MediaToolkit.py -A
   ```

## Workflow

1. When you run the script, it will prompt you for the input folder path.
2. The script analyzes the folder contents and identifies supported media files.
3. You'll be asked to specify output formats and compression levels (if applicable).
4. The script processes each file, displaying progress and success/error messages.
5. Processed files are saved in a new "converted_media" or "converted_fonts" folder.

## Supported Formats

- **Images**: PNG, JPG, JPEG, GIF, BMP
- **Videos**: MP4, AVI, MOV, MKV
- **Fonts**: TTF, OTF, WOFF, WOFF2


## Notes

- Ensure you have necessary permissions to read from the input folder and write to the output folder.
- Video conversion requires FFmpeg to be installed and accessible in your system's PATH.
- Font conversion is handled separately from other media files and has its own set of options.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.