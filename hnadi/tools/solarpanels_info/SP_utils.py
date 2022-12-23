import omni.ui as ui


# Data Manipulation Utils
def map_data(data, min1, max1, min2, max2):
    ratio = abs(data - min1) / (max1 - min1)
    if ratio > 1:
        ratio == 1
    mapped_data = min2 + ratio * (max2 - min2)
    return mapped_data


# UI Colors Utils
# def hex_to_color(hex: int) -> tuple:
#     # convert Value from int
#     red = hex & 255
#     green = (hex >> 8) & 255
#     blue = (hex >> 16) & 255
#     alpha = (hex >> 24) & 255
#     rgba_values = [red, green, blue, alpha]
#     return rgba_values

# def _interpolate_color(hex_min: int, hex_max: int, intep):
#     max_color = hex_to_color(hex_max)
#     min_color = hex_to_color(hex_min)
#     color = [int((max - min) * intep) + min for max, min in zip(max_color, min_color)]
#     return (color[3] << 8 * 3) + (color[2] << 8 * 2) + (color[1] << 8 * 1) + color[0]

# def get_gradient_color(value, max, colors):
#     step_size = len(colors) - 1
#     step = 1.0/float(step_size)
#     percentage = value / float(max)

#     idx = (int) (percentage / step)
#     if idx == step_size:
#         color = colors[-1]
#     else:
#         color = _interpolate_color(colors[idx], colors[idx+1], percentage)
#     return color

# def generate_byte_data(colors):
#     data = []
#     for color in colors:
#         data += hex_to_color(color)

#     _byte_provider = ui.ByteImageProvider()
#     _byte_provider.set_bytes_data(data, [len(colors), 1])
#     return _byte_provider

# def build_gradient_image(colors, height, style_name):
#     byte_provider = generate_byte_data(colors)
#     ui.ImageWithProvider(byte_provider, fill_policy= ui.IwpFillPolicy.IWP_STRETCH, height=height, name=style_name)
#     return byte_provider