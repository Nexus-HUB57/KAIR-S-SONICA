from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

root = Path('/home/ubuntu/KAIR-S-SONICA')
files = sorted((root/'assets/video/keyframes').glob('*.png')) + sorted((root/'assets/video/plates').glob('*.png'))
thumb_w, thumb_h = 420, 260
margin, label_h, cols = 18, 36, 2
rows = (len(files)+cols-1)//cols
sheet = Image.new('RGB', (cols*(thumb_w+margin)+margin, rows*(thumb_h+label_h+margin)+margin), '#111217')
d = ImageDraw.Draw(sheet)
for i, path in enumerate(files):
    x = margin + (i%cols)*(thumb_w+margin)
    y = margin + (i//cols)*(thumb_h+label_h+margin)
    im = Image.open(path).convert('RGB')
    im = ImageOps.fit(im, (thumb_w, thumb_h), method=Image.Resampling.LANCZOS)
    sheet.paste(im, (x,y))
    d.text((x,y+thumb_h+6), path.name[:54], fill='#f2f2f2')
(root/'artifacts/video/validation').mkdir(parents=True, exist_ok=True)
sheet.save(root/'artifacts/video/validation/ktd_dynamic_keyframe_sheet.jpg', quality=92)
