# Discord Image Resizer

This utility makes it easy to resize images that are too large to send on Discord to a size that is appropriate for sending on Discord.

## Usage

```
usage: discord-resize [-h] [-s SIZE] [-i INC] [-n PATH] [-o PATH]

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  the desired size in bytes for the image, default 8000000
  -i INC, --inc INC     the percentage of the starting dimensions to remove on each pass, default 5
  -n PATH, --in PATH    a path to an image to process, defaults to the contents of the clipboard
  -o PATH, --out PATH   the output path for the processed image, defaults to the clipboard
```

## Installation

```sh
$ git clone github.com/nathan-fiscaletti/discord-image-resizer.git
$ cd discord-image-resizer
$ pip3 install -e .
```

You can now run the script from anywhere you have a command line.

```sh
# Copy an image to your clipboard first
$ discord-resize
```

## Example

```
C:\Users\Nathan\git-repos\discord-image-resizer>discord-resize
Resizing image... (66355254 bytes)
Resized Image!    (5972022 bytes) in 0.7866390705108643 seconds

Clipboard Image Updated!

C:\Users\Nathan\git-repos\discord-image-resizer>
```
