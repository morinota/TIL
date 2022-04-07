# datatime.timedelta()関数

日付の加算・減算を行うには、datetime.timedelta()関数を使用する。

```python
>>> import datetime
>>> d = datetime.datetime.now()
>>> d
datetime.datetime(2012, 4, 18, 06, 29, 28, 538000)

>>> d + datetime.timedelta(days=3) #3日加算
datetime.datetime(2012, 4, 21, 06, 29, 28, 538000)

>>> d - datetime.timedelta(hours=3) #3時間減算
datetime.datetime(2012, 4, 18, 03, 29, 28, 538000)
```

引数は以下の通り。

```python
timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
```

timedeltaでは月の加算減算はできず、サードパーティ製ライブラリのpython-dateutil.relativedeltaを使うとできるらしい。
日付に月単位で加算減算する (relativedelta) | Python Snippets(https://python.civic-apps.com/add-month-relativedelta/)

## 参考

https://python.civic-apps.com/timedelta/
