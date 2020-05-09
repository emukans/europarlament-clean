import json
import sys

source_dir = sys.argv[1]

with open(source_dir + 'mscoco/annotations lv full/cap_val_2017.json', 'r') as lv_source,\
        open(source_dir + 'mscoco/annotations en/captions_val2017.json', 'r') as en_source,\
        open(source_dir + 'mscoco/annotations en/en-lv-annotations.json', 'w') as dest_file:
    lv_captions = json.load(lv_source)
    en_captions = json.load(en_source)
    coco_data = []

    for en_cap in en_captions.get('annotations'):
        lv_cap = [cap for cap in lv_captions.get('annotations') if cap.get('id') == en_cap.get('id')][0]
        image = [cap for cap in en_captions.get('images') if cap.get('id') == en_cap.get('image_id')][0]

        coco_data.append({
            'en': en_cap.get('caption').strip().lower(),
            'lv': lv_cap.get('caption').strip().lower(),
            'image': image.get('flickr_url'),
        })

    json.dump(coco_data, dest_file)


with open(source_dir + 'mscoco/annotations en/en-lv-annotations.json', 'r') as file:
    captions = json.load(file)

    print(len(captions))
