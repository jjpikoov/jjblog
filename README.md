# jjblog
My own blogging platform written with Flask and Foundation Framework.

<br>

<h3>Installation</h3>
```bash
git clone https://github.com/jjpikoov/jjblog.git jjblog
cd jjblog
virtualenv venv
. venv/bin/active
pip install Flask
```
<br>

<h3>Configuration</h3>
First of all, please edit config.py file (ProductionConfig class variables).
Then change this line in main.py from:
```python
app.config.from_object('config.DevConfig')
```
to
```python
app.config.from_object('config.ProductionConfig')
```

<br>

<h3>Starting application</h3>
```bash
python main.py
```
<br>

<h3>Screenshots</h3>

![screenshot_2016-01-19_12-27-49](https://cloud.githubusercontent.com/assets/3046087/12417416/43b5282c-bea8-11e5-9504-19a35e909fdb.png)
<br>
![screenshot_2016-01-19_12-22-50](https://cloud.githubusercontent.com/assets/3046087/12417451/78b896bc-bea8-11e5-9be4-04a6cc374ffd.png)
<br>
![screenshot_2016-01-19_12-22-20](https://cloud.githubusercontent.com/assets/3046087/12417433/61d5b204-bea8-11e5-960e-325ccce92568.png)
<br>
![screenshot_2016-01-19_12-28-47](https://cloud.githubusercontent.com/assets/3046087/12417444/7008bfd8-bea8-11e5-88c8-de4119a51039.png)
<br>
![screenshot_2016-01-19_12-24-37](https://cloud.githubusercontent.com/assets/3046087/12417456/81cc0270-bea8-11e5-961e-591548df0832.png)
