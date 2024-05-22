
# Add when testing outside of node:
# import torch
# image1 = torch.randn(3, 3, 3)
# text1 = ""
# text2 = ""

from sklearn.cluster import KMeans
import webcolors

pixels = image1.view(-1, image1.shape[-1]).numpy() # torch already imported
colors = KMeans(n_clusters=5).fit(pixels).cluster_centers_ * 255
complementary_colors = [[(255 - main_colors[i]) % 256 for i in range(3)] for main_colors in colors]
original_colors = [[(main_colors[i]) for i in range(3)] for main_colors in colors]

def get_color_name(color):
    color_tuple = (int(color[0]), int(color[1]), int(color[2]))
    closest_name = None
    min_distance = float("inf")
    for name, color in webcolors.CSS3_HEX_TO_NAMES.items():
        distance = sum(abs(a - b) for a, b in zip(color_tuple, webcolors.hex_to_rgb(name)))
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return webcolors.CSS3_HEX_TO_NAMES[closest_name]


original_palette = ", ".join([get_color_name(color) for color in original_colors])
complement_palette = ", ".join([get_color_name(color) for color in complementary_colors])

print(f"Original colors: {original_palette}\nComplementary colors: {complement_palette}")
text1.to(f"A painting with a color palette of {complement_palette} colors.")
