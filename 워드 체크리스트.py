import os
import tkinter as tk
from tkinter import messagebox, filedialog
import win32com.client as win32

class WordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Document Checker")
        self.root.geometry("600x400")

        self.input_file = None
        self.output_file = None
        self.word_app = None
        self.doc = None

        self.checklist = [
            {"question": "날짜를 바꾸었는가?", "key": "DATE_PLACEHOLDER", "replacement": "2024-06-19"},
            {"question": "출발 시간과 도착시간은 확인하였는가?", "key": "TIME_PLACEHOLDER", "replacement": "09:00 - 18:00"},
            {"question": "팀리더는 맞는가?", "key": "LEADER_PLACEHOLDER", "replacement": "John Doe"},
            {"question": "이동계획은 맞는가?", "key": "PLAN_PLACEHOLDER", "replacement": "Confirmed"}
        ]

        self.current_check_index = 0

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        load_button = tk.Button(frame, text="Load Document", command=self.load_document)
        load_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.root, text="No document loaded", pady=10)
        self.status_label.pack()

    def load_document(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if not file_path:
            return

        try:
            self.input_file = file_path
            self.output_file = file_path.replace(".docx", "_modified.docx")
            
            # MS 워드 애플리케이션을 시작하고 문서를 엽니다.
            self.word_app = win32.gencache.EnsureDispatch('Word.Application')
            self.word_app.Visible = True
            self.doc = self.word_app.Documents.Open(file_path)
            
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.check_elements()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the document: {e}")

    def check_elements(self):
        if self.current_check_index < len(self.checklist):
            self.show_checklist(self.checklist[self.current_check_index])
        else:
            self.validate_document()

    def validate_document(self):
        for item in self.checklist:
            for paragraph in self.doc.Paragraphs:
                if item["key"] in paragraph.Range.Text:
                    paragraph.Range.Text = paragraph.Range.Text.replace(item["key"], item["replacement"])

            for table in self.doc.Tables:
                for row in table.Rows:
                    for cell in row.Cells:
                        for paragraph in cell.Range.Paragraphs:
                            if item["key"] in paragraph.Range.Text:
                                paragraph.Range.Text = paragraph.Range.Text.replace(item["key"], item["replacement"])

        self.doc.SaveAs(self.output_file)
        self.doc.Close()
        self.word_app.Quit()
        messagebox.showinfo("Success", "All elements are validated and replaced.")
        self.status_label.config(text="Document validated and saved.")

    def show_checklist(self, item):
        checklist_window = tk.Toplevel(self.root)
        checklist_window.title("Checklist")
        checklist_window.geometry("400x200")
        checklist_window.attributes("-topmost", True)

        label = tk.Label(checklist_window, text=item["question"])
        label.pack(pady=10)

        yes_button = tk.Button(checklist_window, text="예", command=lambda: self.checklist_response(checklist_window, True))
        yes_button.pack(side=tk.LEFT, padx=20, pady=20)

        no_button = tk.Button(checklist_window, text="아니오", command=lambda: self.checklist_response(checklist_window, False))
        no_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def checklist_response(self, window, response):
        if response:
            self.current_check_index += 1
            window.destroy()
            self.check_elements()
        else:
            messagebox.showwarning("Warning", "Please ensure all items are correctly updated before proceeding.")
            window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordCheckerApp(root)
    root.mainloop()
