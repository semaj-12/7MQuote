import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from processors import pdf_processor, cad_processor, ai_estimator

class App:
    def __init__(self, root):
        self.root = root
        root.title("Local File Upload & AI Estimation")
        root.geometry("600x600")
        
        self.selected_file = None
        
        self.file_label = tk.Label(root, text="No file selected", wraplength=400)
        self.file_label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)
        
        self.process_button = tk.Button(root, text="Process File", command=self.process_file)
        self.process_button.pack(pady=5)
        
        self.result_text = scrolledtext.ScrolledText(root, width=70, height=20)
        self.result_text.pack(pady=10)
        
        self.estimate_button = tk.Button(root, text="Estimate Cost", command=self.estimate_cost)
        self.estimate_button.pack(pady=5)
        
    def select_file(self):
        filetypes = [("Supported Files", "*.dwg;*.dxf;*.rvt;*.pdf")]
        self.selected_file = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        if self.selected_file:
            self.file_label.config(text=f"Selected: {os.path.basename(self.selected_file)}")
        else:
            self.file_label.config(text="No file selected")
            
    def process_file(self):
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file to process.")
            return
        
        ext = os.path.splitext(self.selected_file)[1].lower()
        self.result_text.delete("1.0", tk.END)
        
        if ext == ".pdf":
            result = pdf_processor.process_pdf(self.selected_file)
            self.result_text.insert(tk.END, "PDF Extraction Results:\n")
            self.result_text.insert(tk.END, f"Extracted Text:\n{result.get('text', '')}\n")
            self.result_text.insert(tk.END, f"Number of Images Extracted: {len(result.get('images', []))}\n")
        elif ext == ".dxf":
            result = cad_processor.process_dxf(self.selected_file)
            self.result_text.insert(tk.END, "DXF Extraction Results:\n")
            self.result_text.insert(tk.END, f"{result}\n")
        elif ext in [".dwg", ".rvt"]:
            self.result_text.insert(tk.END, f"Local processing for {ext} files is not supported.\nPlease use APS integration for these file types.\n")
        else:
            self.result_text.insert(tk.END, "Unsupported file type.")
            
    def estimate_cost(self):
        # Placeholder: Use the extracted text from the result_text widget as input for the AI estimator.
        extracted_data = self.result_text.get("1.0", tk.END)
        estimate = ai_estimator.estimate_cost(extracted_data)
        self.result_text.insert(tk.END, f"\nEstimated Cost: {estimate}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
