import os
import shutil
import yaml
import uuid
import argparse

def merge_datasets(dataset1_dir, dataset2_dir, output_dir):
    """
    Merges two YOLO format datasets into a single dataset.
    Handles class index remapping and renaming files to prevent collisions.
    """
    print(f"Merging {dataset1_dir} and {dataset2_dir} into {output_dir}...")
    
    # Ensure output directory structure
    for split in ['train', 'valid', 'test']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)
        
    # Read data.yaml
    yaml1_path = os.path.join(dataset1_dir, 'data.yaml')
    yaml2_path = os.path.join(dataset2_dir, 'data.yaml')
    
    if not os.path.exists(yaml1_path) or not os.path.exists(yaml2_path):
        print("Error: Both datasets must contain a data.yaml file.")
        return
        
    with open(yaml1_path, 'r') as f:
        data1 = yaml.safe_load(f)
    with open(yaml2_path, 'r') as f:
        data2 = yaml.safe_load(f)
        
    classes1 = data1.get('names', [])
    classes2 = data2.get('names', [])
    
    # If names is a dictionary (like {0: 'gun', 1: 'knife'}), convert to list
    if isinstance(classes1, dict):
        classes1 = [classes1[k] for k in sorted(classes1.keys())]
    if isinstance(classes2, dict):
        classes2 = [classes2[k] for k in sorted(classes2.keys())]
        
    # Merge class lists
    merged_classes = list(classes1)
    
    # Create mapping for dataset 2's classes
    class_mapping2 = {} # {old_id: new_id}
    for old_id, class_name in enumerate(classes2):
        if class_name in merged_classes:
            class_mapping2[old_id] = merged_classes.index(class_name)
        else:
            merged_classes.append(class_name)
            class_mapping2[old_id] = len(merged_classes) - 1
            
    print(f"Dataset 1 classes: {classes1}")
    print(f"Dataset 2 classes: {classes2}")
    print(f"Merged classes: {merged_classes}")
    
    # Write merged data.yaml
    merged_data = {
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': len(merged_classes),
        'names': merged_classes
    }
    with open(os.path.join(output_dir, 'data.yaml'), 'w') as f:
        yaml.dump(merged_data, f, default_flow_style=False)
        
    # Function to copy files and remap labels
    def process_dataset(dataset_dir, class_mapping=None):
        for split in ['train', 'valid', 'test']:
            idx = 1
            img_dir = os.path.join(dataset_dir, split, 'images')
            lbl_dir = os.path.join(dataset_dir, split, 'labels')
            
            if not os.path.exists(img_dir) or not os.path.exists(lbl_dir):
                continue
                
            for img_file in os.listdir(img_dir):
                # Use a unique ID to prevent name collisions between datasets
                unique_id = str(uuid.uuid4())[:8]
                img_ext = os.path.splitext(img_file)[1]
                base_name = os.path.splitext(img_file)[0]
                
                new_basename = f"{base_name}_{unique_id}"
                new_img_file = new_basename + img_ext
                new_lbl_file = new_basename + ".txt"
                
                old_lbl_file = base_name + ".txt"
                old_lbl_path = os.path.join(lbl_dir, old_lbl_file)
                
                # Copy image
                shutil.copy2(
                    os.path.join(img_dir, img_file),
                    os.path.join(output_dir, split, 'images', new_img_file)
                )
                
                # Copy and process label
                if os.path.exists(old_lbl_path):
                    with open(old_lbl_path, 'r') as f:
                        lines = f.readlines()
                        
                    new_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            # Remap class id if mapping exists
                            if class_mapping is not None and class_id in class_mapping:
                                new_class_id = class_mapping[class_id]
                            else:
                                new_class_id = class_id # Unchanged (for dataset 1)
                                
                            parts[0] = str(new_class_id)
                            new_lines.append(" ".join(parts) + "\n")
                            
                    with open(os.path.join(output_dir, split, 'labels', new_lbl_file), 'w') as f:
                        f.writelines(new_lines)
                
                if idx % 500 == 0:
                    print(f"Processed {idx} images from {dataset_dir}/{split}...")
                idx += 1
                
    print("\nProcessing Dataset 1...")
    process_dataset(dataset1_dir, class_mapping=None)
    
    print("\nProcessing Dataset 2 (with class remapping)...")
    process_dataset(dataset2_dir, class_mapping=class_mapping2)
    
    print(f"\nSuccessfully merged datasets into: {output_dir}")
    print("You can now zip this output folder and upload it to Google Colab!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two YOLO datasets.")
    parser.add_argument("--d1", required=True, help="Path to first dataset (e.g. real weapons)")
    parser.add_argument("--d2", required=True, help="Path to second dataset (e.g. toy weapons)")
    parser.add_argument("--out", required=True, help="Path to output merged dataset")
    args = parser.parse_args()
    
    merge_datasets(args.d1, args.d2, args.out)
