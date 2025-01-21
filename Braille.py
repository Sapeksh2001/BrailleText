import customtkinter as ctk
import cv2
import pytesseract
from tkinter import filedialog, messagebox

def TextToBraille(input_text):
    # Braille Unicode patterns
    braille_map = {
        'a': '\u2801', 'b': '\u2803', 'c': '\u2809', 'd': '\u2819', 'e': '\u2811',
        'f': '\u280B', 'g': '\u281B', 'h': '\u2813', 'i': '\u280A', 'j': '\u281A',
        'k': '\u2805', 'l': '\u2807', 'm': '\u280D', 'n': '\u281D', 'o': '\u2815',
        'p': '\u280F', 'q': '\u281F', 'r': '\u2817', 's': '\u280E', 't': '\u281E',
        'u': '\u2825', 'v': '\u2827', 'w': '\u283A', 'x': '\u282D', 'y': '\u283D',
        'z': '\u2835', ' ': ' '
    }
    
    # Numbers with prefix ⠼
    number_prefix = '\u283C'
    number_map = {
        '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819', '5': '\u2811',
        '6': '\u280B', '7': '\u281B', '8': '\u2813', '9': '\u280A', '0': '\u281A'
    }

    # Convert to Braille
    braille_output = ''
    for ch in input_text.lower():
        if ch.isdigit():
            braille_output += number_prefix + number_map[ch]
        else:
            braille_output += braille_map.get(ch, '?')

    return braille_output


def CaptureTextFromWebcam():
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Press 's' to capture or 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image.")
            break
        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite("captured_image.png", frame)
            cap.release()
            cv2.destroyAllWindows()
            try:
                text = pytesseract.image_to_string("captured_image.png")
                return text
            except Exception as e:
                messagebox.showerror("Error", f"OCR failed: {e}")
                return None
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None


def ExtractTextFromImageFile():
    file_path = filedialog.askopenfilename(title="Select Image File", 
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return None
    try:
        img = cv2.imread(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        messagebox.showerror("Error", f"OCR failed: {e}")
        return None


def ConvertText():
    input_text = text_input.get("1.0", ctk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Input text is empty!")
        return
    braille_output = TextToBraille(input_text)
    output_text.delete("1.0", ctk.END)
    output_text.insert(ctk.END, braille_output)


def ConvertFromWebcam():
    extracted_text = CaptureTextFromWebcam()
    if extracted_text:
        text_input.delete("1.0", ctk.END)
        text_input.insert(ctk.END, extracted_text)


def ConvertFromImageFile():
    extracted_text = ExtractTextFromImageFile()
    if extracted_text:
        text_input.delete("1.0", ctk.END)
        text_input.insert(ctk.END, extracted_text)


# Initialize CustomTkinter GUI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Text to Braille Converter")
app.geometry("700x500")

# Input Frame
input_frame = ctk.CTkFrame(app, corner_radius=10)
input_frame.pack(pady=10, padx=10, fill="x")

input_label = ctk.CTkLabel(input_frame, text="Input Text:", font=("Arial", 14))
input_label.pack(anchor="w", pady=5)

text_input = ctk.CTkTextbox(input_frame, height=100)
text_input.pack(fill="x", pady=5)

convert_button = ctk.CTkButton(input_frame, text="Convert to Braille", command=ConvertText)
convert_button.pack(pady=5)

# Output Frame
output_frame = ctk.CTkFrame(app, corner_radius=10)
output_frame.pack(pady=10, padx=10, fill="x")

output_label = ctk.CTkLabel(output_frame, text="Braille Output:", font=("Arial", 14))
output_label.pack(anchor="w", pady=5)

output_text = ctk.CTkTextbox(output_frame, height=100)
output_text.pack(fill="x", pady=5)

# Options Frame
options_frame = ctk.CTkFrame(app, corner_radius=10)
options_frame.pack(pady=10, padx=10, fill="x")

webcam_button = ctk.CTkButton(options_frame, text="Capture from Webcam", command=ConvertFromWebcam)
webcam_button.pack(side="left", padx=10, pady=10)

image_button = ctk.CTkButton(options_frame, text="Select Image File", command=ConvertFromImageFile)
image_button.pack(side="left", padx=10, pady=10)

# Run the app
app.mainloop()
