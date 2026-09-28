'''
Main file, just testing for now
This code was/is copy and pasted boiler plate
'''
import asyncio
import os
import base64
import pathlib
import io
from openrouter import OpenRouter
import cv2
from PIL import Image

RUN_AI = True
BLUR_IMAGE = True
BLUR_STRENGTH = 101

current_num_path = pathlib.Path(r'data\current_num.dat')
images = pathlib.Path("images_to_use")
files = [item for item in images.iterdir() if item.is_file()]
file_count = len(files)
result_list = []
tasks = []

system_prompt = 'You are an image-classification model whose task is to distinguish between a cat and a dog. Examine the image and identify: 1. Whether the animal is a cat or a dog. 2. Its breed, if the breed can be identified with reasonable confidence. Your response must be lowercase and contain exactly 2 parts in this order:<animal> <breed> If the animal or breed cannot be determined, use unknown instead'


def get_name(file:pathlib.Path):
    '''Returns the name of the file'''
    cur_name = file.name
    for j in range(len(cur_name)-1, -1, -1):
        if cur_name[j] == '_':
            return cur_name[0:j].lower()

def encode_image(path):
    '''AI generated function'''
    #Clears metadata
    with Image.open(path) as img:
        with io.BytesIO() as buffer:
            img.getexif().clear()
            img.save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

def encode_blurred_image(path, blur_strength):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # (5, 5) is the kernel size; 0 lets OpenCV auto-calculate the standard deviation (sigmaX)
    img_blur = cv2.GaussianBlur(img, (blur_strength, blur_strength), 0)
    success, encoded_img = cv2.imencode('.jpeg', img_blur)
    with io.BytesIO() as buffer:
        buffer.write(encoded_img.tobytes())
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

def write_results(results):
    num = update_get_current_num()
    with open(current_num_path.parent/f"result{num}.txt", "a") as f:
        f.write(f"Blur: {BLUR_STRENGTH} State: {BLUR_IMAGE}\n")
        for i in results:
            f.write(str(i)+'\n')

def update_get_current_num():
    current_num_path.parent.mkdir(parents=True, exist_ok=True)
    current_num_path.touch()
    with open(current_num_path, "r") as f:
        num_string = f.read()
        if num_string.isdigit():
            num = str(int(num_string)+1)
        else:
            print("the data file is not a number")
            print("Remaking file at 2...")
            num = '2'
    with open(current_num_path, "w") as f:
        f.write(num)
        return int(num)-1

async def send_image(count, name, file):
    if BLUR_IMAGE:
        base64_image = encode_blurred_image(file, BLUR_STRENGTH)
    else:
        base64_image = encode_image(file)
    data_url = f"data:image/jpeg;base64,{base64_image}"

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Identify the animal"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
            ]
        }
    ]
    if RUN_AI:
        try:
            client = OpenRouter(
                api_key = os.environ["API_KEY"],
                server_url = os.environ["URL"]
            )

            response = client.chat.send(
                model="google/gemini-3-flash-preview",
                messages=messages
            )
        except Exception as e:
            print(f"There was an exception {e}")
            print("Writing results...")
            write_results(result_list)
            return
        print(f"File {file} ({count}/{file_count}) done!")
        result_list.append((count, name, response.choices[0].message.content))

async def main():
    count = 0
    name = ""
    async with asyncio.TaskGroup() as tg:
        for file in files:
            count += 1
            name = get_name(file)
            task = tg.create_task(send_image(count,name,file))
            tasks.append(task)
            print(f"Testing file {file} ({count}/{file_count})")
    print("Done, writing results...")
    write_results(result_list)

if __name__ == "__main__":
    asyncio.run(main())
