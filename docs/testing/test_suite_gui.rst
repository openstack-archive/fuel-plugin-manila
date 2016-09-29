=========
GUI tests
=========


GUI defaults test
-----------------


ID
##

manila_gui_defalts


Description
###########

Check default settings for Manila Plugin via GUI.


Complexity
##########

core


Steps
#####

    1. Upload plugins to the master node and install.
    2. Create a new environment.
    3. Verify default settings for Plugin:
       Plugin is enabled, generic driver is enabled, default values for the
       rest fields are present.


Expected results
################

All steps must be completed successfully, without any errors.


GUI field validation test
-------------------------


ID
##

manila_gui_validation


Description
###########

Check validation messages for Manila Plugin settings via GUI.


Complexity
##########

core


Steps
#####

    1. Upload plugins to the master node and install.
    2. Create a new environment.
    3. Check validation for setting Image name.
    4. Check validation for setting NetApp server Hostname.
    5. Check validation for setting NetApp transport type.
    6. Check validation for setting NetApp server port.
    7. Check validation for setting NetApp username.
    8. Check validation for setting NetApp password.
    9. Check validation for setting NetApp volume aggregate.
    10. Check validation for setting NetApp pattern for aggregation names.
    11. Check validation for setting NetApp pattern for storage port names.


Expected results
################

All steps must be completed successfully, without any errors.
