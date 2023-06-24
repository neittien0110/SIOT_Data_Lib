# SIOT_Data_Lib

## How to setup

```dos
   pip install -r requirements.txt
```

## How to run

```dos
   python .\GetData.py
```

## Just for System Admin

### Assign mysql account

```mysql
GRANT SELECT on siot.DeviceDataBySlug TO 'siot_getdata'@'%';
REVOKE SELECT on siot.DeviceData FROM 'siot_getdata'@'%'
GRANT execute on  PROCEDURE DeviceDataBySlug TO 'siot_getdata'@'%';
FLUSH PRIVILEGES;
```
