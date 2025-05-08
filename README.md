# ⚽ Center Circle Keypoint Annotator

This is a simple, easy-to-use desktop annotation tool that helps you manually label **keypoints around the center circle** of a football/soccer field from video frames or images.

---

## 📦 Features

- Click to add keypoints
- Drag keypoints to adjust
- Undo/reset keypoints
- Navigate freely between images
- Save annotations to a `.json` file
- See helpful instructions and warnings on screen

---

## 🖥 How to Use

### 1. 📁 Start the Tool

- Double-click the provided `.exe` file (e.g., `annotator.exe`)
- A folder selection window will appear
- Choose the folder **that contains your image frames**

### 2. ✍️ Annotate Images

Once the tool opens:

- **Left-click** to add keypoints (add at least **17** total — 16 around the circle and 1 center)
- **Click and drag** a keypoint to adjust its position
- You’ll see live instructions and keypoint counts on the screen

### 3. 💡 Keyboard Controls

| Key     | Action                            |
|---------|-----------------------------------|
| `Left-click` | Add a keypoint              |
| `Drag`  | Move a keypoint                   |
| `u`     | Undo last keypoint                |
| `r`     | Reset (clear all keypoints)       |
| `n`     | Go to next image                  |
| `p`     | Go to previous image              |
| `s`     | Save current annotations          |
| `Esc`   | Exit and auto-save current image  |

---

## 🧾 Annotation Format

- Saved in a file called `annotations.json` **inside the selected image folder**
- JSON format stores keypoints per image filename:
```json
{
  "image1.jpg": [[x1, y1], [x2, y2], ..., [x17, y17]],
  "image2.jpg": [[x1, y1], [x2, y2], ..., [x17, y17]]
}
