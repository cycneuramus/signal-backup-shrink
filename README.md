## Overview

This is a companion script to [signalbackup-tools](https://github.com/bepaald/signalbackup-tools) that reduces the size of a Signal backup by processing message attachments of the following file types:

+ `.jpg, .png` (resized and compressed)
+ `.gif, .mp4, .mkv, .3gp` (replaced with a collage of keyframes)

Using this method, I was able to reduce my Signal backup size by about 80% (from 4GB to 800MB) without having to delete anything and thus lose context in the message history.

## Dependencies

+ [signalbackup-tools](https://github.com/bepaald/signalbackup-tools)
+ [vcsi](https://github.com/amietn/vcsi)
+ [filetype](https://pypi.org/project/filetype)
+ [pillow](https://pypi.org/project/Pillow)

## Usage

1. Dump the unencrypted backup components to disk:

`signalbackup-tools [backupfile] [password] --output [directory]`

2. Process message attachments:

`signal-backup-shrink.py [directory]`

3. Re-encrypt backup with processed attachments:

`signalbackup-tools [directory] --replaceattachments -o OUTPUT.backup -op [password]`

## Limitations

Currently, `signalbackup-tools` [only supports replacing attachments with images](https://github.com/bepaald/signalbackup-tools/issues/68#issuecomment-1138812152). Hence, it is not possible to 

+ process audio files (such as voice recordings)
+ replace gifs or videos with smaller versions
+ optimize PDFs or other documents
