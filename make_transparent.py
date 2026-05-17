from PIL import Image
import shutil

# backup original
shutil.copy("logo.png", "logo_backup.png")

img = Image.open("logo.png").convert("RGBA")
pixels = img.load()

for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = pixels[x, y]
        # We assume the logo is mostly black text/icon on white background
        # Any white pixel becomes transparent.
        # To avoid white halos around the black text, we can turn the pixel black
        # and set its alpha to how dark it was.
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        
        # If it's a completely white pixel, gray is 255 -> alpha is 0
        # If it's a black pixel, gray is 0 -> alpha is 255
        # This perfectly preserves anti-aliased edges for a black logo.
        # To preserve colors if there are any non-gray pixels, we can keep the original color
        # but just scale the alpha by how close it is to white. 
        # But multiplying color by alpha might be tricky. Let's just use the original color 
        # and set alpha based on how far it is from white.
        # If r,g,b are all 255 -> alpha 0.
        
        # A simple method that preserves color:
        # Distance to white: 255 - (r+g+b)/3
        # Let's map 255 to 0 alpha, and anything darker than 200 to 255 alpha (fully opaque)
        if gray > 240:
            pixels[x, y] = (r, g, b, 0)
        else:
            # We need to fade the alpha for edges.
            # 240 -> 0 alpha
            # 200 -> 255 alpha
            if gray > 200:
                alpha = int(255 * (240 - gray) / 40)
                # To avoid white halo, push color towards black
                pixels[x, y] = (0, 0, 0, alpha)
            else:
                pixels[x, y] = (r, g, b, 255)

img.save("logo.png")
