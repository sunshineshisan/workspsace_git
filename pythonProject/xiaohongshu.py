import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO

# 创建文件夹以保存爬取到的图片
if not os.path.exists('D:/Backup/Downloads/xiaohongshu_images'):
    os.makedirs('D:/Backup/Downloads/xiaohongshu_images')

# 爬取的目标URL
url = 'https://www.xiaohongshu.com/user/profile/5936abe55e87e77bd51d28c5'  # 这里是示例URL，请根据需要进行修改

# 发送请求获取页面
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code != 200:
    print(f'Failed to retrieve the page: {response.status_code}')
else:
    print('Page retrieved successfully!')

# 解析页面
soup = BeautifulSoup(response.text, 'html.parser')

downloaded_images = 0
min_size = 20  # 最小尺寸，单位：像素
target_count = 100  # 目标数量

# 修改选择器以找到所有的img标签
for img_tag in soup.find_all('img'):
    print(img_tag)
    if downloaded_images >= target_count:
        break  # 达到目标数量则停止

    img_url = img_tag.get('src')
    print(f'Found image URL: {img_url}')  # 输出找到的图片URL，便于调试
    if img_url:
        try:
            img_response = requests.get(img_url, stream=True)
            img_response.raise_for_status()  # 确保请求成功

            # 使用PIL检查图片尺寸
            img = Image.open(BytesIO(img_response.content))
            width, height = img.size

            # 检查图片是否满足尺寸要求
            if width >= min_size and height >= min_size:
                # 保存图片
                img_name = os.path.join('xiaohongshu_images', img_url.split('/')[-1])
                with open(img_name, 'wb') as f:
                    f.write(img_response.content)
                print(f'Downloaded: {img_name}')
                downloaded_images += 1
                print(f'Total images downloaded: {downloaded_images}')  # 实时跟踪下载数量

        except Exception as e:
            print(f'Error downloading {img_url}: {e}')

print(f'Download completed! Total images downloaded: {downloaded_images}')