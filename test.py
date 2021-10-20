from PIL import Image
import os 

filename_list = os.listdir('icon/')
# filename_list = ['shadow.png']
print(filename_list)

for filename in filename_list:

    img = Image.open('icon/'+filename)
    img_resize = img.resize((80,60))
    img_resize.save('iconimg/'+filename)