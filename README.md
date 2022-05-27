## Overview

This is a companion script to [signalbackup-tools](https://github.com/bepaald/signalbackup-tools) that reduces the size of a Signal backup by processing message attachments of the following file types:

+ `.jpg, .png` (resized and compressed)
+ `.gif, .mp4, .mkv, .3gp` (replaced with a collage of keyframes)

Using this method, I was able to reduce my Signal backup size by about ~80% (from 4GB to 800MB).

## Dependencies

+ [signalbackup-tools](https://github.com/bepaald/signalbackup-tools)
+ [vcsi](https://github.com/amietn/vcsi)
+ [filetype](https://pypi.org/project/filetype)

## Usage

1. Dump the unencrypted backup components to disk:
`signalbackups-tools [input] [password] --output [outputdirectory]`

2. Process message attachments:
`signal-backup-shrink.py [outputdirectory]`

3. Re-encrypt backup with processed attachments:
`signalbackup-tools [outputdirectory] --replaceattachments -o OUTPUT.backup -op [password]`
