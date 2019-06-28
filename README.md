# XBOS Driver Development Tools

These tools will use a formatted csv file to generate a proto file, xbos message, as well as a plugin for simple devices.

## Generate entity setup all permissions:

For wattnode (Enter nothing for usage)
```
../setup_entity.sh wattnode $NAMESPACE_HASH $NAMESPACE
```

## Generate proto file with message name
```
python proto_gen.py dark_sky.csv Dark_Sky_State dark_sky.proto
python proto_gen.py .csv Dark_Sky_State dark_sky.proto
```

## Generate Proto files for Dark Sky weather current and predictive
```
python proto_gen.py weather_current.csv Weather_Current_State weather_current.proto
python proto_gen.py weather_prediction.csv Weather_Prediction_State weather_prediction.proto
```


## Generate message section for parker,weather_current,weather_prediction,wattnode

```
python message_gen.py weather_current.csv > weather_current.message
python message_gen.py weather_prediction.csv > weather_prediction.message
python message_gen.py parker_full.csv > parker_full.message 
python message_gen.py wattnode.csv > wattnode.message 
```


After making the proto file and message components of the driver, the message needs to be added in iot.proto in  XBOSIoTDeviceState so it will become a field
```
message XBOSIoTDeviceState {
    // current time at device/service
    //unit:ns
    uint64 time = 1;
    // unique identifier for this request; used to line up with device state requests
    int64 requestid = 2;
    // any error that occured since the last device report. If requestid above is non-zero,
    // then this error corresponds to the request with the given requestid
    string error = 3;

    // XBOS IoT devices
    Thermostat thermostat = 4;
    Meter meter = 5;
    Light light = 6;
    EVSE evse = 7;
    //WeatherStation weather_station = 8;
    //WeatherStationPrediction weather_station_prediction = 9;
    ParkerState parker_state = 8;
    Weather_Current_State current_weather = 9;
}
```
## Make all generated files
```
make proto
make proto-py
```
## Generate plugin for ingester
The name for the message should be the same as the first part of the message name 

### Example:
In the iot.proto example above,
Weather_Current_State current_weather = 9;eather_Current_State current_weather = 9; 

Weather_Current_State would be the correct message name!

### Example:
python plugin_gen.py parker_full.csv ParkerState parker_plugin.go
python plugin_gen.py wattnode.csv WattnodeState wattnode_plugin.go

When figuring out the message name for the ingester plugin look at iot.proto
Field names may also change, I adapted the code to work names with underscores, but if it fails because of field names look at the device drivers pb.go in ~/xboswave/proto/

