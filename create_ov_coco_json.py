import json

annotations_path = 'datasets/coco/annotations/'
save_path = 'datasets/coco-zero-shot/'

with open(annotations_path + 'instances_train2017.json', 'r') as fin:
    coco_train_anno_all = json.load(fin)
with open(annotations_path + 'instances_train2017.json', 'r') as fin:
    coco_train_anno_seen = json.load(fin)
with open(annotations_path + 'instances_train2017.json', 'r') as fin:
    coco_train_anno_unseen = json.load(fin)
with open(annotations_path + 'instances_val2017.json', 'r') as fin:
    coco_val_anno_all = json.load(fin)
with open(annotations_path + 'instances_val2017.json', 'r') as fin:
    coco_val_anno_seen = json.load(fin)
with open(annotations_path + 'instances_val2017.json', 'r') as fin:
    coco_val_anno_unseen = json.load(fin)

with open('mscoco_seen_classes.json', 'r') as fin:
    labels_seen = json.load(fin)
with open('mscoco_unseen_classes.json', 'r') as fin:
    labels_unseen = json.load(fin)

print(len(labels_seen), len(labels_unseen))
labels_all = [item['name'] for item in coco_val_anno_all['categories']]
print(set(labels_seen) - set(labels_all))
print(set(labels_unseen) - set(labels_all))

class_id_to_split = {}
class_name_to_split = {}
for item in coco_val_anno_all['categories']:
    if item['name'] in labels_seen:
        class_id_to_split[item['id']] = 'seen'
        class_name_to_split[item['name']] = 'seen'
    elif item['name'] in labels_unseen:
        class_id_to_split[item['id']] = 'unseen'
        class_name_to_split[item['name']] = 'unseen'

def filter_annotation(anno_dict, split_name_list):
    filtered_categories = []
    for item in anno_dict['categories']:
        if class_id_to_split.get(item['id']) in split_name_list:
            item['split'] = class_id_to_split.get(item['id'])
            filtered_categories.append(item)
    anno_dict['categories'] = filtered_categories

    filtered_images = []
    filtered_annotations = []
    useful_image_ids = set()
    for item in anno_dict['annotations']:
        if class_id_to_split.get(item['category_id']) in split_name_list:
            filtered_annotations.append(item)
            useful_image_ids.add(item['image_id'])
    for item in anno_dict['images']:
        if item['id'] in useful_image_ids:
            filtered_images.append(item)
    anno_dict['annotations'] = filtered_annotations
    anno_dict['images'] = filtered_images


filter_annotation(coco_train_anno_seen, ['seen'])
filter_annotation(coco_train_anno_unseen, ['unseen'])
filter_annotation(coco_train_anno_all, ['seen', 'unseen'])
filter_annotation(coco_val_anno_seen, ['seen'])
filter_annotation(coco_val_anno_unseen, ['unseen'])
filter_annotation(coco_val_anno_all, ['seen', 'unseen'])
print(len(coco_val_anno_seen['categories']), len(coco_val_anno_unseen['categories']),
      len(coco_val_anno_all['categories']))

import os
os.makedirs(save_path)

with open(save_path+'instances_train2017_seen_2.json', 'w') as fout:
    json.dump(coco_train_anno_seen, fout)
with open(save_path+'instances_train2017_unseen_2.json', 'w') as fout:
    json.dump(coco_train_anno_unseen, fout)
with open(save_path+'instances_train2017_all_2.json', 'w') as fout:
    json.dump(coco_train_anno_all, fout)
with open(save_path+'instances_val2017_seen_2.json', 'w') as fout:
    json.dump(coco_val_anno_seen, fout)
with open(save_path+'instances_val2017_unseen_2.json', 'w') as fout:
    json.dump(coco_val_anno_unseen, fout)
with open(save_path+'instances_val2017_all_2.json', 'w') as fout:
    json.dump(coco_val_anno_all, fout)