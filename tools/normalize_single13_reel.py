from pathlib import Path
from PIL import Image

source = Path('/home/ubuntu/KAIR-S-SONICA-repo/outputs/single_13/static_reels/ktd-what-happens-in-vegas-02-irmaos.png')
tmp = source.with_suffix('.normalized.png')
target = (1440, 2560)

with Image.open(source) as image:
    if image.size != target:
        resized = image.resize(target, Image.Resampling.LANCZOS)
        resized.save(tmp, format='PNG', optimize=True)
        tmp.replace(source)
    print(f'{source}: {target[0]}x{target[1]}')
