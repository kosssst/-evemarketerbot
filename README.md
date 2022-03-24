# -evemarketerbot

***Works only on Windows***

This bot allows to transfer prices from Eve Marketer to Google Sheets.

### **Requirements:**

- Python

### **How to install:**

- **Download code**
``` 
git clone https://github.com/kostyamed/-evemarketerbot.git
```

- **Create Google application for each type of item what you want to track:**

https://medium.com/daily-python/python-script-to-edit-google-sheets-daily-python-7-aadce27846c0

after this you need to have .json files with login data

- **Enter folder**
```
cd -evemarketerbot
```

- **Create folder for your login files with name `keys`**
```
mkdir keys
```

- **Install libraries:**
```
pip install -r requirements.txt
```

- **Move files, which you got earlier, to folder `keys`**

- **Create table on Google Sheets**

- **Edit `config.py` and files in `json/` for you**

- **Start program:**
```
python main.py
```