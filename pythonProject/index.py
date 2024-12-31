import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import base64
# 设置User-Agent，防止被网站拒绝访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 要爬取的链接
url = "https://www.xiaohongshu.com/user/profile/602770240000000001000456?xsec_token=&xsec_source=pc_note"  # 示例链接

# 发送请求
response = requests.get(url, headers=headers)

# 解析网页
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的图片链接
images = soup.find_all(class_='')

# 图片保存路径
save_dir = 'xiaohongshu_images'
os.makedirs(save_dir, exist_ok=True)

def traverse_directory(path):
    for root, dirs, files in os.walk(path):
        print(f"当前目录: {root}")
        for dir_name in dirs:
            print(f"  文件夹: {dir_name}")
        for index, file_name in enumerate(files, start=1):
            # print(f"  文件: {root}/{file_name}")
            print(root+'/'+file_name)
            crop_bottom(root+file_name, root+'1/'+str(index)+'.jpg', 35)
def crop_bottom(image_path, output_path, crop_height):
        # 打开图片
        img = Image.open(image_path)

        # 获取图片的宽度和高度
        width, height = img.size
        print(height - crop_height)
        # 计算裁剪区域
        crop_area = (0, 0, width, height - crop_height)

        # 裁剪图片
        cropped_img = img.crop(crop_area)

        # 保存裁剪后的图片
        cropped_img.save(output_path)
        print(f"已成功裁剪底部 {crop_height} 像素并保存为 {output_path}")
    # 使用示例

def download_image(url, min_size_kb, index):
    try:
        # 先获取图片的头信息
        response = requests.head(url)
        response.raise_for_status()  # 检查请求是否成功

        # 获取图片的大小（以字节为单位）
        content_length = int(response.headers.get('Content-Length', 0))
        size_kb = content_length / 1024  # 转换为KB

        # 检查图片大小
        if size_kb < min_size_kb:
            print(f"图片大小 {size_kb:.2f} KB 小于 {min_size_kb} KB，跳过下载。")
            return

        # 下载图片
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        with open('F:/Users/98/Documents/爬虫数据/模特'+str(index)+'.png', "wb") as file:
            file.write(response.content)
        print("图片已成功下载并保存！")

    except Exception as e:
        print(f"下载失败: {e}")

# 下载图片
# for index, img in images:
for index, img in enumerate(images, start=1):

    print(index)
    img_url = img.get('src')
    if img_url.find("data:") == -1:
        print(img_url)
        download_image(img_url, 30, index)
#裁切图片
# traverse_directory("F:/Users/98/Documents/爬虫数据/")
        # 发送请求获取图片
        # response = requests.get(img_url)
        #
        # # 检查请求是否成功
        # if response.status_code == 200:
        #     # 保存图片到本地
        #     with open('F:/Users/98/Documents/爬虫数据/模特'+str(index)+'.png', "wb") as file:
        #         file.write(response.content)
        #     print("图片已成功下载并保存！")
        # else:
        #     print("下载图片失败，状态码:", response.status_code)
    # 保存为文件
    # with open('F:/Users/98/Documents/爬虫数据/模特'+str(index)+'.png', 'wb') as f:
    #     print("图像已保存为 output_image.png")
    # if img_url:
    #     img_name = os.path.join(save_dir, img_url.split('/')[-1])
    #     img_data = requests.get(img_url, headers=headers).content
    #     with open(img_name, 'wb') as f:
    #         f.write(img_data)
    #         print(f'Downloaded: {img_name}')