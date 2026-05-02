# plymouth
sp0rk1s's Plymouth Loading Screen

# Python Usage Tutorial
General example
```py
from plymouth import Plymouth

loading_screen = Plymouth()

job = loadingscreen.start("service", "description")
# Loading happens here
job.finish()

loading_screen.end()
```
```diff
         Starting plymouth.service - (v1.0.0) Enabling plymouth for the application...
[  OK  ] Started plymouth.service - (v1.0.0) Enabling plymouth for the application.
[  OK  ] Finished plymouth.service - (v1.0.0) Enabling plymouth for the application.

# Job example

         Starting service - description...
[  OK  ] Started service - description.

# Loading happens here

[  OK  ] Finished service - description.

# Job concluded

         Starting plymouth-quit.service - Disabling plymouth for the application...
[  OK  ] Started plymouth-quit.service - Disabling plymouth for the application.
[  OK  ] Finished plymouth-quit.service - Disabling plymouth for the application.
# This is properly colored colored when used
```

2nd example
```py
job = loadingscreen.start("example.service", "a description")
time.sleep(8)
job.fail()
```
```diff
         Starting example.service - a description...
[  OK  ] Started example.service - a description.
[  *** ] Job example.service running (8s / no limit)
[FAILED] Failed example.service - a description.
```
