import os
import cv2
import imgaug as ia
import numpy as np
import pandas as pd
from imgaug import augmenters as iaa
import matplotlib.pyplot as plt
from itertools import repeat
import jinja2
from jinja2 import Environment, Template
from jinja2 import FileSystemLoader
import cv2
from config import TARGET_DIR, FILL_UP_TO

np.random.bit_generator = np.random._bit_generator

# uses the mapped.csv that datamapper.py generated
def read_csv():
    df = pd.read_csv('mapped.csv', delimiter=',')
    return df


#called in main: categorizes the data into bins, returns dataframe with categorised data
def cat_df(df):
    bins = [-np.inf, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, np.inf]

    #bin names
    labels = [
        '-1.0 to -0.8',
        '-0.8 to -0.6',
        '-0.6 to -0.4',
        '-0.4 to -0.2',
        '-0.2 to 0.0',
        '0.0 to 0.2',
        '0.2 to 0.4',
        '0.4 to 0.6',
        '0.6 to 0.8',
        '0.8 to 1.0'
    ]
    df['cat'] = pd.cut(df['ang_z'], bins=bins, labels=labels, include_lowest=True)
    data = {
        'lin_x': df['lin_x'],
        'ang_z': df['ang_z'],
        'cat': df['cat'],
        'path': df['file_path']}

    new = pd.DataFrame(data, columns=['lin_x', 'ang_z', 'cat', 'path'])
    pd.set_option('max_colwidth', 30)
    return new

# the acutal function that changes the picture. Add more if you like.
def aug_gauss(image):
    ia.seed(4)
    img = cv2.imread(image)
    image_aug = iaa.AdditiveGaussianNoise(scale=(10, 15)).augment_image(img)

    return image_aug


# called in main: counts how many items are in each category
def count_cats(df_cat, collumn):
    counts = df_cat[collumn].value_counts(dropna=False)
    return counts

# finds the missing data
def count_missing(count, num):
    new = []

    for value in count.values:
        if value <= num:
            new.append(-(value - num))
        else:
            new.append(0)

    with_missing = pd.DataFrame({'cat': count.index, 'occ': count.values, 'missing': new})

    return with_missing

# helper for augement()
def filter_missing(cat, pred):
    df_filtered = cat[(cat['cat'] == pred)]
    return df_filtered

# this uses a jinja2 template to generate a yaml for all the augmented data
def to_yaml(path, var_lin_x, var_aug_z, var_path):
    template = '''
- timestamp: 'aug'
  action_messages:
    /nr/engine/input/actions:
      linear:
        y: 0.0
        x: {{ lin_x }}
        z: 0.0
      angular:
        y: 0.0
        x: 0.0
        z: {{ ang_z }}
  camera_messages:
  - {{ path }}'''

    filename = 'augmented3' + '.yaml'
    with open(os.path.join(path, filename), 'a+') as f:
        temp = jinja2.Template(template)
        yaml_data = temp.render(lin_x=var_lin_x, ang_z=var_aug_z, path=var_path)
        f.write(yaml_data)
        f.close()

# this is the augentation pipeline, steps are marked in the code
# 1. for each category of with_missing > 0 in with missing und finde alle mit dieser kathegorie in cat
# 2. aus df von 1. , entnehme random bilder aus bis with_missing erfullt ist
# 3. augmentiere jedes bild und generiere einen eintrag in ein yaml
def augment(cat, counted_missing):
    path = TARGET_DIR
    add_pic_path = 'zed/left/image_raw_color/compressed'

    aug_pics_path = os.path.join(path, add_pic_path)

    if os.path.exists(path):
        os.system('rm -rf ' + path)
        os.makedirs(aug_pics_path)
    else:
        os.makedirs(aug_pics_path)

    for index, row in counted_missing[(counted_missing.missing > 0)].iterrows():

        # 1
        df_filtered = filter_missing(cat, row['cat'])

        # 2
        count = 0
        for _ in repeat(None, counted_missing['missing'][index]):
            path_to_augmented = (add_pic_path + '/aug_' + str(index) + '_' + str(count) + '.jpg')

            selected = cat.sample(1)

            image_to_augment = selected.iloc[0]['path']

            augmented_image = aug_gauss(image_to_augment)

            cv2.imwrite(path_to_augmented, augmented_image)
            count += 1

            # 3
            to_yaml(path, selected.iloc[0]['lin_x'], selected.iloc[0]['ang_z'], path_to_augmented)
            print(path_to_augmented)


def main():

    # 1 categorise data
    cat = cat_df(csv)

    # 2 counts how many items are in each category
    counted = count_cats(cat, 'cat')

    # 3 checks how many are missing to fill up to FILL_UP_TO
    counted_missing = count_missing(counted, FILL_UP_TO)

    #optional: a dataframe to csv that you can visualise if you like
    counted_missing.to_csv('numbers.csv',index=False)

    # 4 augement all the data you are missing
    augment(cat, counted_missing)


if __name__ == "__main__":
    main()
