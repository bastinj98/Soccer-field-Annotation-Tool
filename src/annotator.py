import cv2
import os
import json
import argparse

RADIUS = 8
MIN_KEYPOINTS = 17
ANNOTATION_FILE = "annotations.json"

keypoints = []
drag_idx = -1
image_idx = 0
images = []
annotations = {}

def draw_overlay(img, kp_count):
    display = img.copy()
    
    status_text = f"Keypoints: {kp_count} | "
    status_text += "Warning: atleast 17 keypoints need: 16 for periphery and 1 for center!" if kp_count < MIN_KEYPOINTS else "OK"

    help_text = [
        "Controls:",
        "'left-click': Add point, 'drag': to move/adjust point",
        "'u': Undo   'r': Reset",
        "'n': Next   'p': Prev",
        "'u': Undo   'r': Reset",   
        "'s': Save",
        "ESC: Exit"
    ]

    cv2.rectangle(display, (0, 0), (850, 170), (0, 0, 0), -1)  # background
    cv2.putText(display, status_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 255) if kp_count < MIN_KEYPOINTS else (0, 255, 0), 2)

    for i, line in enumerate(help_text):
        cv2.putText(display, line, (10, 40 + 20 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    return display

def draw_keypoints():
    display = draw_overlay(current_image.copy(), len(keypoints))
    for idx, (x, y) in enumerate(keypoints):
        cv2.circle(display, (x, y), RADIUS, (0, 255, 0), -1)
        cv2.putText(display, str(idx), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Annotator", display)

def mouse_callback(event, x, y, flags, param):
    global drag_idx
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (px, py) in enumerate(keypoints):
            if (x - px) ** 2 + (y - py) ** 2 < RADIUS ** 2:
                drag_idx = i
                return
        keypoints.append((x, y))
        draw_keypoints()

    elif event == cv2.EVENT_MOUSEMOVE and drag_idx != -1:
        keypoints[drag_idx] = (x, y)
        draw_keypoints()

    elif event == cv2.EVENT_LBUTTONUP:
        drag_idx = -1

def load_image():
    global current_image, keypoints
    img_name = images[image_idx]
    path = os.path.join(image_folder, img_name)
    current_image = cv2.imread(path)
    keypoints.clear()
    if img_name in annotations:
        keypoints.extend(annotations[img_name])
    draw_keypoints()
    cv2.setMouseCallback("Annotator", mouse_callback)
    print(f"\n🔹 Viewing [{image_idx + 1}/{len(images)}]: {img_name}")

def save_current_annotation():
    annotations[images[image_idx]] = keypoints.copy()
    with open(ANNOTATION_FILE, "w") as f:
        json.dump(annotations, f, indent=2)
    print(f"[✓] Saved {len(keypoints)} keypoints for {images[image_idx]}")

def annotate(image_folder_path):
    global image_folder, images, image_idx

    image_folder = image_folder_path
    images = [f for f in sorted(os.listdir(image_folder)) if f.lower().endswith(('.jpg', '.png'))]
    if not images:
        print("[!] No images found.")
        return

    # Load existing annotations if available
    if os.path.exists(ANNOTATION_FILE):
        with open(ANNOTATION_FILE, "r") as f:
            global annotations
            annotations = json.load(f)

    cv2.namedWindow("Annotator")
    load_image()

    while True:
        key = cv2.waitKey(0)

        if key == ord('n') and image_idx < len(images) - 1:
            save_current_annotation()
            image_idx += 1
            load_image()

        elif key == ord('p') and image_idx > 0:
            save_current_annotation()
            image_idx -= 1
            load_image()

        elif key == ord('u'):
            if keypoints:
                keypoints.pop()
                draw_keypoints()

        elif key == ord('r'):
            keypoints.clear()
            draw_keypoints()

        elif key == ord('s'):
            save_current_annotation()

        elif key == 27:  # ESC
            save_current_annotation()
            print("[✔] Exiting.")
            break

    cv2.destroyAllWindows()

# Run it
#annotate("C:\Dev\logoplacement\Arsenal vs Man Utd_01_SpiderCam")  # Change to your image folder path

def main():
    parser = argparse.ArgumentParser(description="Keypoint Annotator Tool for Soccer Center Circle")
    parser.add_argument("folder", type=str, help="Path to folder containing images")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"[!] Folder '{args.folder}' not found.")
        return

    annotate(args.folder)

if __name__ == "__main__":
    main()
