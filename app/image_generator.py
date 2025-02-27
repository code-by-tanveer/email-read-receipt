from PIL import Image, ImageDraw

def generate_read_receipt(read=False):
    img = Image.new("RGB", (50, 50), color="white")
    draw = ImageDraw.Draw(img)

    color = "blue" if read else "gray"
    draw.line((10, 25, 20, 35), fill=color, width=3)
    draw.line((20, 35, 40, 10), fill=color, width=3)

    img_path = "/tmp/receipt.png"
    img.save(img_path)
    return img_path
