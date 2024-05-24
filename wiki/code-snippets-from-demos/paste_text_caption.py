


# --- Picture: example1-caption_composite.png

from PIL import ImageDraw, ImageFont
from torchvision import transforms

def draw_text(text, img_tensor):
    img_pil = transforms.ToPILImage()(img_tensor[0].permute(2, 0, 1))

    draw = ImageDraw.Draw(img_pil)
    font_size = img_tensor.shape[2] // 8
    position = (img_tensor.shape[2] // 3, img_tensor.shape[1] // 3)

    font = ImageFont.load_default().font_variant(size=font_size)
    draw.text(position, text.data, fill="red", font=font)
    
    return transforms.ToTensor()(img_pil).permute(1, 2, 0).unsqueeze(0)

image1.to(draw_text(text1, image1))
image2.to(draw_text(text2, image2))