from PIL import Image, ImageDraw, ImageFont
import os

def create_text_image(text, font_path, font_size, text_color, shadow_color):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError as e:
        print(f"Could not load font from {font_path}: {e}")
        return None

    # Calculate text size
    dummy_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Create image with padding
    padding = 20
    img_width = text_width + (padding * 2)
    img_height = text_height + (padding * 2)
    
    img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw text centered
    text_x = padding - bbox[0]
    text_y = padding - bbox[1]
    
    # Draw Shadow
    draw.text((text_x + 2, text_y + 4), text, font=font, fill=shadow_color)
    
    # Draw Text
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return img

def main():
    base_dir = os.getcwd()
    font_path = os.path.join(base_dir, "assets", "fonts", "EBGaramond.ttf")
    
    if not os.path.exists(font_path):
        print(f"Font file not found: {font_path}")
        return

    output_dir = os.path.join(base_dir, "custom_components", "oblamatik", "brand")
    root_dir = base_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Colors
    # Text: Light Gray (visible on dark) -> (200, 200, 200)
    # But for white background, we need contrast.
    # Compromise: Middle Gray or distinct Shadow.
    # Let's use the color from the YAML: (175, 180, 186) which is a cool gray.
    text_color = (175, 180, 186, 255) 
    shadow_color = (0, 0, 0, 100) # Semi-transparent black shadow
    
    # 1. Generate Logo (Text "Oblamatik")
    print(f"Generating logo@2x.png using font: {font_path}")
    logo_2x = create_text_image("Oblamatik", font_path, 200, text_color, shadow_color)
    
    if logo_2x:
        # Save @2x
        logo_2x.save(os.path.join(output_dir, "logo@2x.png"))
        logo_2x.save(os.path.join(root_dir, "logo@2x.png"))
        
        # Save standard
        target_width = logo_2x.width // 2
        target_height = logo_2x.height // 2
        logo = logo_2x.resize((target_width, target_height), Image.Resampling.LANCZOS)
        logo.save(os.path.join(output_dir, "logo.png"))
        logo.save(os.path.join(root_dir, "logo.png"))
        print("Logos saved.")

    # 2. Generate Icon (Letter "O")
    print(f"Generating icon@2x.png using font: {font_path}")
    # Icon usually needs to be square.
    # Let's generate a large "O" and center it in a square.
    icon_size = 512
    icon_img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon_img)
    
    # Find font size that fits "O" in 512x512
    # Start with 400
    font_size = 450
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), "O", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    # Center
    x = (icon_size - w) // 2 - bbox[0]
    y = (icon_size - h) // 2 - bbox[1]
    
    # Draw Shadow
    draw.text((x + 4, y + 8), "O", font=font, fill=shadow_color)
    # Draw Text
    draw.text((x, y), "O", font=font, fill=text_color)
    
    # Save @2x
    icon_img.save(os.path.join(output_dir, "icon@2x.png"))
    icon_img.save(os.path.join(root_dir, "icon@2x.png"))
    
    # Save standard (256x256)
    icon_std = icon_img.resize((256, 256), Image.Resampling.LANCZOS)
    icon_std.save(os.path.join(output_dir, "icon.png"))
    icon_std.save(os.path.join(root_dir, "icon.png"))
    print("Icons saved.")

if __name__ == "__main__":
    main()
