from tkinter import Tk, Label, Button, filedialog, Frame
from PIL import Image, ImageTk
import numpy as np

class ImageEncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")

        self.frame = Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.label = Label(self.frame, text="Select an image to encrypt/decrypt:")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.attach_button = Button(self.frame, text="Attach File", command=self.attach_file)
        self.attach_button.grid(row=1, column=0, pady=5)

        self.encrypt_button = Button(self.frame, text="Encrypt Image", command=self.encrypt_image, state="disabled")
        self.encrypt_button.grid(row=1, column=1, pady=5)

        self.decrypt_button = Button(self.frame, text="Decrypt Image", command=self.decrypt_image, state="disabled")
        self.decrypt_button.grid(row=1, column=2, pady=5)

        self.image_label = Label(self.frame)
        self.image_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.status_label = Label(self.frame, text="", fg="green")
        self.status_label.grid(row=3, column=0, columnspan=3)

        self.encrypted_image_path = None  # Initialize encrypted image path

    def attach_file(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.label.config(text=f"Selected image: {self.image_path}")
            self.show_image(self.image_path)
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="normal")
            self.status_label.config(text="")

    def show_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((200, 200))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

    def encrypt_image(self):
        if hasattr(self, 'image_path'):
            encryption_key = 50  # Example encryption key (you can change this)
            encrypted_image = self.encrypt_image_op(self.image_path, encryption_key)
            encrypted_image.show()
            self.status_label.config(text="Image encrypted successfully.", fg="green")
        else:
            self.status_label.config(text="Please attach an image first.", fg="red")

    def decrypt_image(self):
        if self.encrypted_image_path:
            decryption_key = 50  # Example decryption key (same as encryption key)
            decrypted_image = self.decrypt_image_op(self.encrypted_image_path, decryption_key)
            decrypted_image.show()
            self.status_label.config(text="Image decrypted successfully.", fg="green")
        else:
            self.status_label.config(text="Please encrypt an image first.", fg="red")

    def encrypt_image_op(self, image_path, encryption_key):
        image = Image.open(image_path)
        image_array = np.array(image, dtype=np.uint8)  # Ensure image array is of type uint8
        encryption_key = np.uint8(encryption_key)  # Ensure encryption key is of type uint8

        # Perform encryption with modulo operation to ensure values stay within 0-255 range
        encrypted_array = (image_array.astype(np.uint16) + encryption_key) % 256
        encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8))
        self.encrypted_image_path = "encrypted_image.png"
        encrypted_image.save(self.encrypted_image_path)  # Save the encrypted image for decryption
        return encrypted_image

    def decrypt_image_op(self, encrypted_image_path, decryption_key):
        encrypted_image = Image.open(encrypted_image_path)
        encrypted_array = np.array(encrypted_image, dtype=np.uint8)  # Ensure image array is of type uint8
        decryption_key = np.uint8(decryption_key)  # Ensure decryption key is of type uint8

        # Perform decryption with modulo operation to ensure values stay within 0-255 range
        decrypted_array = (encrypted_array.astype(np.uint16) - decryption_key) % 256
        decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8))
        return decrypted_image

root = Tk()
app = ImageEncryptionGUI(root)
root.mainloop()
