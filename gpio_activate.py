import subprocess

subprocess.run(["echo 450 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Forward
subprocess.run(["echo 421 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Reverse
subprocess.run(["echo 447 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Confirm
subprocess.run(["echo 448 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Subfeature_Exit
#subprocess.run(["echo 501 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Walk&Go_See(Old_GPIO)
subprocess.run(["echo 500 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Walk&Go_See(New_GPIO)
subprocess.run(["echo 502 >/sys/class/gpio/export"], shell=True, executable="/bin/bash")#Voice_Feature_Exit