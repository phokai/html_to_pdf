import tkinter as tk
from tkinter import filedialog, messagebox
import asyncio
from pyppeteer import launch
import os

class HTMLToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML'den PDF'ye Dönüştürücü")
        self.html_files = []

        self.create_widgets()

    def create_widgets(self):
        self.select_files_button = tk.Button(self.root, text="HTML Dosyalarını ve Kayıt Klasörünü Seç", command=self.select_files_and_output_dir)
        self.select_files_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Çıkış", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def select_files_and_output_dir(self):
        self.html_files = filedialog.askopenfilenames(filetypes=[("HTML dosyaları", "*.html")])
        if self.html_files:
            self.output_dir = filedialog.askdirectory()
            if self.output_dir:
                messagebox.showinfo("Seçilen Dosyalar ve Kayıt Klasörü", f"{len(self.html_files)} dosya seçildi. Dosyalar şu klasöre kaydedilecek: {self.output_dir}")
                self.convert_to_pdf()
            else:
                self.html_files = []  # Kayıt klasörü seçilmezse html_files'i sıfırla
                messagebox.showwarning("Eksik Bilgi", "Lütfen bir kayıt klasörü seçin.")
        else:
            messagebox.showwarning("Eksik Bilgi", "Lütfen HTML dosyalarını seçin.")

    def convert_to_pdf(self):
        if not self.html_files or not self.output_dir:
            messagebox.showwarning("Eksik Bilgi", "Lütfen HTML dosyalarını ve bir kayıt klasörü seçin.")
            return

        asyncio.run(self.convert_files())

    async def convert_files(self):
        browser = await launch()
        for html_file in self.html_files:
            output_file = os.path.join(self.output_dir, os.path.basename(html_file).replace('.html', '.pdf'))
            page = await browser.newPage()
            await page.goto(f'file://{html_file}')
            await page.pdf({'path': output_file})
        await browser.close()

        messagebox.showinfo("Dönüştürme Tamamlandı", "Tüm dosyalar PDF'ye dönüştürüldü.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLToPDFConverter(root)
    root.mainloop()
