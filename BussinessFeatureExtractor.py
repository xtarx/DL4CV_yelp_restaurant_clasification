import pandas as pd
import numpy as np
import os.path
from io import StringIO

PHOTO_TO_BIZ_PATH = 'dataset/train_photo_to_biz_ids.csv'
PHOTO_FEATURES_PATH = 'bottlenecks\\multi_label'
BUSINESS_FEATURES_PATH = 'bottlenecks\\train_business_features'

train_photo_to_biz = pd.read_csv(PHOTO_TO_BIZ_PATH).dropna()

# Temp list containing all images belonging to a certain restaurant
images_of_business = []


def get_numpy_from_txt(path):
    print path
    np_features = np.loadtxt(path, delimiter=',')
    print np_features


for business_id in train_photo_to_biz['business_id']:
    print 'Processing restaurant ', business_id,
    out_path = os.path.join(BUSINESS_FEATURES_PATH, str(business_id) + '.features')
    if os.path.isfile(out_path):
        print ' Already processed'
        continue
    image_features = np.zeros((2048,), dtype='float64')
    images_of_business = 0
    images_not_found = 0
    for position in xrange(len(train_photo_to_biz['business_id'])):
        # append all images from same restaurant.
        if business_id == train_photo_to_biz['business_id'][position]:
            image_id = train_photo_to_biz['photo_id'][position]
            path = os.path.join(PHOTO_FEATURES_PATH, str(image_id) + '.jpg.txt')
            try:
                image_features += np.loadtxt(path, delimiter=',')
                images_of_business += 1
            except IOError as e:
                images_not_found += 1
    print ' - ', images_of_business, ' found ', images_not_found, ' Images missing - saving ...',
    image_features /= images_of_business
    # Save restaurant features
    np.savetxt(out_path, image_features.astype('float32'), delimiter=',')
    print 'done'
