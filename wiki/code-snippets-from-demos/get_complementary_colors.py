# Add when testing outside of node:
import torch

image1 = torch.randn(3, 3, 3)
text1 = ""
text2 = ""

from sklearn.cluster import KMeans
import webcolors


from sklearn.cluster import KMeans
def get_colors(image):
    pixels = image.view(-1, image.shape[-1]).numpy()  # torch already imported
    colors = KMeans(n_clusters=5).fit(pixels).cluster_centers_ * 255
    return colors

def get_complementary_colors(main_colors):
    ret = []
    for colors in main_colors:
        ret.append([(255 - colors[i]) % 256 for i in range(3)])
    return ret
    
def get_color_names(color_list):
    import webcolors
    colors = []
    for color in color_list:
        rgb = (int(color[0]), int(color[1]), int(color[2]))
        c, min_d = None, float("inf")
        for name, color in webcolors.CSS3_HEX_TO_NAMES.items():
            distance = sum(abs(a - b) for a, b in zip(rgb, webcolors.hex_to_rgb(name)))
            if distance < min_d:
                min_d, c = distance, name
        colors.append(webcolors.CSS3_HEX_TO_NAMES[c])
    return ", ".join(colors[:-1]) + " and " + colors[-1]

colors = get_colors(image1)
complementary_colors = get_complementary_colors(colors)
colors = get_color_names(colors)
complementary_colors = get_color_names(complementary_colors)

print(f"Main color palette: {colors}")
print(f"Complementary color palette: {complementary_colors}")

