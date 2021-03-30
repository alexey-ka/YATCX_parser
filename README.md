# YATCX_parser
Yet Another TCX Parser  
yatsx_parser in a more advanced parser of the Garmin data files that was influenced by [python-tcxparser](https://github.com/vkurup/python-tcxparser/).  
The main difference from the rest of the available parser is in the core idea of the project that is connected to the OpenLAPP framework (to be published) that requires interaction with a more low-lever data with more advanced data aggregations.  
Current version extracts the following properties:  
- ```features``` dictionary of the available features in the .tcx file  
- ```has_powers``` flag that shows availability of the power measurements in the files  
- ```powers``` list of the extracted power measurements  
- ```grades``` list of the extracted slope grades in degrees  
- ```distances``` list of the passed distance  
- ```moves``` list of the moves during a single measurement  
- ```low_altitude_distance``` passed distance on a low-altitude (by default, 1500m)  
- ```high_altitude_distance``` passed distance on a high-altitudee (by default, 1500m)  
- ```elevations``` list of the elevations  
- ```total_elevation``` total elevation (or some of the positive climbs)  
- ```heart_rate```  list of the heart rate measurements  
- ```mean_heart_rate``` average heart rate during the session  
- ```speeds```  list of the speeds  
- ```altitudes``` list of the altitudes  
- ```cadences``` list of the cadences
- ```high_altitude_time``` total time on the high-altitude(by default, 1500m)  
- ```total_distance``` total distance passed during the session  
- ```calories``` total calories  
- ```total_time``` total session time  
- ```datetime``` session start time  
- ```date``` session date
- ```get_path(path, namespace)``` Read a value of a random value that could be found in the ```path``` inside of the ```namespace```  
- ```read_xpath_property(xpath_obj, name)```Read a numeric property name in the given xpath_obj object  
  
## Default namespaces  
Default namespaces from Garmin  
| Namespace |-- URI --|  
| ------------- |:-------------:|  
| ns | http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 |
| ns2 | http://www.garmin.com/xmlschemas/UserProfile/v2 |  
| ns3 | http://www.garmin.com/xmlschemas/ActivityExtension/v2 |  
| ns4 | http://www.garmin.com/xmlschemas/ProfileExtension/v1 |  
| ns5 | http://www.garmin.com/xmlschemas/ActivityGoals/v1 |   
| xsi | http://www.w3.org/2001/XMLSchema-instance |  
  

## Init parameters  
```file_name``` **mandatory** parameter with a path to the .tcx file  
```pre_read``` flag that makes a pre-initiation of the data for a quicker access if the same properties are expected to be called many times. *Default: False*  
```params``` dictionary of parameters  
```recovery``` flag to perform data recovery with a linear interpolation. Alternatively set by the ```params```. *Default: True*  
### Default parameters  
By default, the parameters are set as following:  
  
``` 
default_params = {  
    'high_altitude': 1500,  
    'recovery': True  
}
```
That corresopnds to a default min altitude of 1500 meters and replace all the missing values with a linear interplation model.  
   
## Usage  
```
filename = '1.tcx'
tcxparser = TcxParser(filename, pre_read=True)
tcxparser.powers  
# get list of the powers [0,0 ... , 0, 0]  
```

# Compatibility  
| 3.6 | 3.7 | 3.8 | 3.9 |  
| + | + | + | + |  
'+' confirmed compatibility  

# License  
MIT  
# Authors  
Primary author: Aleksei Karetnikov  
