from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image, ImageTk
import pandas as pd
import time

master = Tk()

class App(Tk):

    def __init__(self):

        master.title("Search Product")
        master.resizable(False,False)

        self.icon_img = PhotoImage(file="images/search.png")
        master.iconphoto(False, self.icon_img)

        self.canvas = Canvas(master, width= 500, height=700)
        self.canvas.pack()

        self.top_frame = Frame(master, bg="#262d36", width=455, height=165)
        self.top_frame.place(relx=0.05, rely=0.03)

        self.bottom_frame = Frame(master, bg="#262d36", width= 455, height= 460)
        self.bottom_frame.place(relx = 0.05, rely= 0.3)

        self.search_label = Label(self.top_frame, bg="#262d36", fg= "white", font=("Microsoft YaHei UI Light",14))
        self.search_label.place

        self.search_bar = Entry(self.top_frame, font=("Microsoft YaHei UI Light",14), width=23)
        self.search_bar.place(x = 105, y = 70)

        self.top_label = Label(self.top_frame, bg="#262d36", fg="white" ,font=("Microsoft YaHei UI Light",14), text="Please enter the product name:")
        self.top_label.place(x=96, y = 20)

        amazon_image = Image.open('images/amazon.png').resize((64,64),Image.LANCZOS)
        self.amazon_pic = ImageTk.PhotoImage(amazon_image)
        hb_image = Image.open('images/hepsiburada.jpg').resize((64,64),Image.LANCZOS)
        self.hb_pic = ImageTk.PhotoImage(hb_image)
        n11_image = Image.open('images/n11.png').resize((64,64),Image.LANCZOS)
        self.n11_pic = ImageTk.PhotoImage(n11_image)

        self.amazon_button = Button(self.bottom_frame, bg="#131414", font=("Microsoft YaHei UI Light",14), text="Search in Amazon", command=self.search_amazon, image=self.amazon_pic)
        self.hepsiburada_button = Button(self.bottom_frame,bg="#131414" , font=("Microsoft YaHei UI Light",14), text="Search in HepsiBurada" , command=self.search_hb, image=self.hb_pic)
        self.n11_button = Button(self.bottom_frame,bg="#131414", font=("Microsoft YaHei UI Light",14), text="Search in N11" , command=self.search_n11, image=self.n11_pic)

        self.dir_label = Label(self.bottom_frame, bg="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14), text="Where to save the excel file:")
        self.dir_label.place(x=110,y=20)

        self.dir_button = Button(self.bottom_frame,bg="#131414", fg="white", font=("Microsoft YaHei UI Light",14), text="Directory" , command=self.ask_directory)
        self.dir_button.place(x=180, y=70)

        self.location = Label(self.bottom_frame, bg="#262d36",fg="white", font=("Microsoft YaHei UI Light",14), text="...")
        self.location.place(x=30, y=135)

        self.select_label = Label(self.bottom_frame, bg="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14), text="Select a website:")
        self.select_label.place(x=155,y=310)

        self.amazon_button.place(x=50, y=360)
        self.hepsiburada_button.place(x=190, y=360)
        self.n11_button.place(x=330, y=360)

        self.range_label = Label(self.bottom_frame, bg="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14), text="Select a price range:")
        self.range_label.place(x=140,y=185)

        self.var = IntVar()
        self.all_radio = Radiobutton(self.bottom_frame, text="All", variable=self.var, value=1, bg="#262d36", selectcolor="#262d36" ,fg="white" , font=("Microsoft YaHei UI Light",14),)
        self.all_radio.place(x=20,y=225)
        self.radio1 = Radiobutton(self.bottom_frame, text="0-10 TL", variable=self.var, value=2, bg="#262d36", selectcolor="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14))
        self.radio1.place(x=20, y=265)
        self.radio2 = Radiobutton(self.bottom_frame, text="100-300", variable=self.var, value=3, bg="#262d36", selectcolor="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14))
        self.radio2.place(x=180, y=225)
        self.radio3 = Radiobutton(self.bottom_frame, text="300-500", variable=self.var, value=4, bg="#262d36", selectcolor="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14))
        self.radio3.place(x=180, y=265)
        self.radio4 = Radiobutton(self.bottom_frame, text="500-1000", variable=self.var, value=5, bg="#262d36", selectcolor="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14))
        self.radio4.place(x=340, y=225)
        self.radio5 = Radiobutton(self.bottom_frame, text="1000-∞", variable=self.var, value=6, bg="#262d36", selectcolor="#262d36", fg="white" , font=("Microsoft YaHei UI Light",14))
        self.radio5.place(x=340, y=265)

    def ask_directory(self):
        self.path = filedialog.askdirectory()
        self.location.config(text=self.path)

    def get_keyword(self):
        keyword = self.search_bar.get()
        return keyword

    def create_driver(self, url):
        url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)

    def search_amazon(self):
        value = self.var.get()
        keyword = self.get_keyword()

        if len(keyword) < 3:
            message = "Please enter a word at least 3 characters!"
            messagebox.showerror("Failed!",message)
        elif self.location.cget("text") == "...":
            message = "Please select a location to save the file!"
            messagebox.showerror("Failed!",message)
        elif value == 0:
            message = "Please be sure that you have selected a price range!"
            messagebox.showerror("Failed!",message)
        else:
            url = "https://www.amazon.com.tr/"
            self.create_driver(url = url)
            time.sleep(0.5)
            self.driver.maximize_window()
            search_entry = self.driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            search_entry.send_keys(keyword)
            search_entry.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            product_names = []
            product_prices = []

            product_name_objects = self.driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")
            for product_name in product_name_objects:
                product_names.append(product_name.text)

            product_price_objects = self.driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
            for product_price in product_price_objects:
                product_prices.append(int(float(product_price.text.replace(".",""))))

            df = pd.DataFrame(zip(product_names,product_prices),columns=["Ürün İsimleri","Ürün Fiyatları"])

            if value == 1:
                df = df
            elif value == 2:
                df = df[(df["Ürün Fiyatları"]>=0) & (df["Ürün Fiyatları"]<100)]
            elif value == 3:
                df = df[(df["Ürün Fiyatları"]>=100) & (df["Ürün Fiyatları"]<300)]
            elif value == 4:
                df = df[(df["Ürün Fiyatları"]>=300) & (df["Ürün Fiyatları"]<500)]
            elif value == 5:
                df = df[(df["Ürün Fiyatları"]>=500) & (df["Ürün Fiyatları"]<1000)]
            elif value == 6:
                df = df[(df["Ürün Fiyatları"]>=1000)]

            df.to_excel(f"{self.path}/{keyword}.xlsx",index=False)

            time.sleep(0.5)
            self.driver.close()
            master.destroy()

    def search_hb(self):
        value = self.var.get()
        keyword = self.get_keyword()

        if len(keyword) < 1:
            message = "Please don't leave a blank!"
            messagebox.showerror("Failed!",message)
        elif self.location.cget("text") == "...":
            message = "Please select a location to save the file!"
            messagebox.showerror("Failed!",message)
        elif value == 0:
            message = "Please be sure that you have selected a price range!"
            messagebox.showerror("Failed!",message)
        else:
            url = "https://www.hepsiburada.com/"
            self.create_driver(url = url)
            self.driver.maximize_window()
            search_entry = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div[5]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/input')
            search_entry.send_keys(keyword)
            search_entry.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            product_names = []
            product_prices = []

            product_name_objects = self.driver.find_elements(By.XPATH, "//h3[@data-test-id='product-card-name']")

            for product_name in product_name_objects:
                product_names.append(product_name.text)

            product_price_objects = self.driver.find_elements(By.XPATH, "//div[@data-test-id='price-current-price']")

            for product_price in product_price_objects:
                product_prices.append(int(float(product_price.text.replace(".","").replace(",",".").replace(" TL",""))))

            df = pd.DataFrame(zip(product_names,product_prices),columns=["Ürün İsimleri", "Ürün Fiyatları"])

            if value == 1:
                df = df
            elif value == 2:
                df = df[(df["Ürün Fiyatları"]>=0) & (df["Ürün Fiyatları"]<100)]
            elif value == 3:
                df = df[(df["Ürün Fiyatları"]>=100) & (df["Ürün Fiyatları"]<300)]
            elif value == 4:
                df = df[(df["Ürün Fiyatları"]>=300) & (df["Ürün Fiyatları"]<500)]
            elif value == 5:
                df = df[(df["Ürün Fiyatları"]>=500) & (df["Ürün Fiyatları"]<1000)]
            elif value == 6:
                df = df[(df["Ürün Fiyatları"]>=1000)]

            df.to_excel(f"{self.path}/{keyword}.xlsx",index=False)

            time.sleep(0.5)
            self.driver.close()
            master.destroy()

    def search_n11(self):
        value = self.var.get()
        keyword = self.get_keyword()

        if len(keyword) < 1:
            message = "Please don't leave a blank!"
            messagebox.showerror("Failed!",message)
        elif self.location.cget("text") == "...":
            message = "Please select a location to save the file!"
            messagebox.showerror("Failed!",message)
        elif value == 0:
            message = "Please be sure that you have selected a price range!"
            messagebox.showerror("Failed!",message)
        else:
            url = "https://www.n11.com/"
            self.create_driver(url = url)
            self.driver.maximize_window()
            search_entry = self.driver.find_element(By.XPATH, '//*[@id="searchData"]')
            search_entry.send_keys(keyword)
            search_entry.send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            product_names = []
            product_prices = []

            product_name_objects = self.driver.find_elements(By.XPATH, "//h3[@class='productName']")
            for product_name in product_name_objects:
                product_names.append(product_name.text)

            product_price_objects = self.driver.find_elements(By.XPATH, "//span[@class='newPrice cPoint priceEventClick']")
            for product_price in product_price_objects:
                product_prices.append(int(float(product_price.text.replace(" TL","").replace(".","").replace(",","."))))

            df = pd.DataFrame(zip(product_names,product_prices),columns=["Ürün İsimleri", "Ürün Fiyatları"])

            if value == 1:
                df = df
            elif value == 2:
                df = df[(df["Ürün Fiyatları"]>=0) & (df["Ürün Fiyatları"]<100)]
            elif value == 3:
                df = df[(df["Ürün Fiyatları"]>=100) & (df["Ürün Fiyatları"]<300)]
            elif value == 4:
                df = df[(df["Ürün Fiyatları"]>=300) & (df["Ürün Fiyatları"]<500)]
            elif value == 5:
                df = df[(df["Ürün Fiyatları"]>=500) & (df["Ürün Fiyatları"]<1000)]
            elif value == 6:
                df = df[(df["Ürün Fiyatları"]>=1000)]

            df.to_excel(f"{self.path}/{keyword}.xlsx",index=False)

            time.sleep(0.5)

            self.driver.close()
            master.destroy()

app = App()
master.mainloop()