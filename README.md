# demkalmyk

```
pyinstaller --name=DEM `
            --icon=import/icon.ico `
            --onefile `
            --windowed `
            --clean `
            --collect-all mysql.connector `
            --add-data "import/photos;import/photos" `
            --add-data "import/icon.ico;import/" `
            --add-data "import/icon.png;import/" `
            --add-data "import/picture.png;import/" `
            --add-data "import/icon.jpg;import/" `
            src/main.py
```