# import pyheif
# from PIL import Image

# def convert_heic_to_jpg(heic_path, jpg_path):
#     heif_file = pyheif.read(heic_path)
#     image = Image.frombytes(
#         heif_file.mode, 
#         heif_file.size, 
#         heif_file.data,
#         "raw",
#         heif_file.mode,
#         heif_file.stride,
#     )
#     image.save(jpg_path, "JPEG")

# # Example usage
# convert_heic_to_jpg("input.heic", "output.jpg")
