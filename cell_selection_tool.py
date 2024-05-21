import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from skimage import io

class ImageViewer:
    def __init__(self, nucleus_image, width, height, brightfield_image):
        self.root = tk.Tk()
        self.root.title("NFAT Translocation Analysis Tool")

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack(side=tk.LEFT)

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.listbox_frame = tk.Frame(self.frame)
        self.listbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.select_roi)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.btn_add_roi = tk.Button(self.root, text="Add ROI", command=self.add_roi)
        self.btn_add_roi.pack(pady=5)

        self.btn_delete_roi = tk.Button(self.root, text="Delete ROI", command=self.delete_roi)
        self.btn_delete_roi.pack(pady=5)

        self.show_hide_button = tk.Button(self.root, text="Show/Hide Brightfield Image", command=self.toggle_image)
        self.show_hide_button.pack(pady=5)

        self.btn_continue = tk.Button(self.root, text="Continue with next image", command=self.continue_next_image)
        self.btn_continue.pack(pady=5)

        self.btn_cancel = tk.Button(self.root, text="Cancel", command=quit)
        self.btn_cancel.pack(pady=5)

        self.roi_active = False
        self.roi_points = []
        self.rois = []
        self.selected_roi_index = None

        self.nucleus_image = nucleus_image
        self.nucleus_image = Image.fromarray(self.nucleus_image)
        self.show_image()

        self.width = width
        self.height = height

        self.is_brightfield_shown = False

        self.brightfield_image = brightfield_image
        self.brightfield_image = Image.fromarray(self.brightfield_image)

    def show_image(self, brightfield = False):
        if brightfield:
            image = self.brightfield_image
        else:
            image = self.nucleus_image

        image = image.resize((500, 500))  # Resize image to fit canvas
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.draw_rois()

    def add_roi(self):
        if not self.roi_active:
            self.roi_active = True
            self.canvas.bind("<Button-1>", self.start_roi)

    def start_roi(self, event):
        self.roi_points = [(event.x, event.y)]
        self.canvas.bind("<Motion>", self.draw_roi)
        self.canvas.bind("<ButtonRelease-1>", self.end_roi)

    def draw_roi(self, event):
        if self.roi_points:
            x0, y0 = self.roi_points[0]
            x1, y1 = event.x, event.y
            self.canvas.delete("roi")
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="roi")

    def end_roi(self, event):
        x0, y0 = self.roi_points[0]
        x1, y1 = event.x, event.y
        self.roi_points.append((x1, y1))
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.rois.append(self.roi_points)
        self.roi_points = []
        self.roi_active = False
        self.draw_rois()
        self.update_listbox()

    def draw_rois(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        for i, roi_points in enumerate(self.rois, start=1):
            if self.selected_roi_index is not None and i == self.selected_roi_index:
                color = "blue"
            else:
                color = "red"
            self.canvas.create_rectangle(*roi_points, outline=color, tags="roi")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, roi_points in enumerate(self.rois, start=1):
            self.listbox.insert(tk.END, f"ROI {i}: {roi_points}")

    def toggle_image(self):
        self.is_brightfield_shown = not self.is_brightfield_shown
        self.show_image(brightfield=self.is_brightfield_shown)

    def select_roi(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.selected_roi_index = selected_index[0] + 1
            self.draw_rois()

    def delete_roi(self):
        if self.selected_roi_index:
            del self.rois[self.selected_roi_index - 1]
            self.selected_roi_index = None
            self.update_listbox()
            self.draw_rois()

    def continue_next_image(self):
        self.root.destroy()

    def save_roi(self):
        print("ROIs saved:", self.rois)

    def return_rois(self):
        roi_normalized = []
        for roi in self.rois:
            minr, minc, maxr, maxc = int(roi[0][1]*self.height/500), int(roi[0][0]*self.width/500), int(roi[1][1]*self.height/500), int(roi[1][0]*self.width/500)
            roi_normalized.append((minr, minc, maxr, maxc))
        return roi_normalized

    def run_mainloop(self):
        self.root.mainloop()

# Create GUI
# app = ImageViewer()
# root.mainloop()
