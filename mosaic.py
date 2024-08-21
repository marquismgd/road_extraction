import os
import rasterio
from rasterio.merge import merge

def merge_tiff_files_in_folder(folder_path, output_path):
    image_list = []
    profile = None

    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'):
            file_path = os.path.join(folder_path, filename)

            # 读取 TIFF 文件
            with rasterio.open(file_path) as src:
                if profile is None:
                    profile = src.profile  # 获取第一个图像的属性作为输出图像的属性
                image_list.append(src)

    # 合并图像
    merged_image, transform = merge(image_list)

    # 更新元数据
    profile.update({"height": merged_image.shape[1],
                    "width": merged_image.shape[2],
                    "transform": transform})

    # 保存合并后的图像
    with rasterio.open(output_path, "w", **profile) as dest:
        dest.write(merged_image)

# 使用函数进行镶嵌
merge_tiff_files_in_folder(r"H:\Columbus\mosaic\gis\small_dataset\test_image_copy_skeleton", r"H:\Columbus\mosaic\gis\small_dataset\mosaic\test_image_copy_skeleton.tif")
