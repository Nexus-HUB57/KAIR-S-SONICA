from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path('/home/ubuntu/KAIR-S-SONICA')
files = [
    root/'assets/persona/artista-principal-diamante.png',
    root/'assets/persona/ktd-visual-master.png',
    root/'assets/persona/ktd-expression-rooftop.png',
    root/'assets/persona/ktd-expression-stage.png',
    root/'assets/persona/ktd-expression-street.png',
    root/'assets/persona/ktd-expression-studio.png',
    root/'assets/persona/ktd-physical-turnaround-sheet.png',
    root/'assets/video/promos/fire-in-the-flood-v4-teaser-8s-vertical.mp4',
]
thumb_w, thumb_h = 360, 240
margin, label_h = 18, 42
cols = 2
rows = (len(files)+cols-1)//cols
sheet = Image.new('RGB', (cols*(thumb_w+margin)+margin, rows*(thumb_h+label_h+margin)+margin), '#101014')
d = ImageDraw.Draw(sheet)
for i, path in enumerate(files):
    x = margin + (i%cols)*(thumb_w+margin)
    y = margin + (i//cols)*(thumb_h+label_h+margin)
    if path.suffix.lower() in {'.mp4','.mov','.webm'}:
        import subprocess
        frame = root/'tmp_contact_frame.jpg'
        subprocess.run(['ffmpeg','-y','-ss','2','-i',str(path),'-frames:v','1','-vf','scale=360:240',str(frame)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        im = Image.open(frame).convert('RGB')
    else:
        im = Image.open(path).convert('RGB')
    im = ImageOps.fit(im, (thumb_w,thumb_h), method=Image.Resampling.LANCZOS)
    sheet.paste(im, (x,y))
    d.text((x,y+thumb_h+6), path.name[:48], fill='#f3f3f3')
sheet.save(root/'artifacts/ktd_visual_contact_sheet.jpg', quality=92)
