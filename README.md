# 1self-sensor-station
Create a sensor station from a Raspberry Pi and some sensors and automatically upload the data to your 1self account

### .env file
In order to run this you'll need to create a .env file in the root directory.

The .env file should have the format, as follows:

```
APP_ID=<get your app id from 1self.co/developers>
APP_SECRET=<get your app secret from 1self.co/developers>
API_URL=https://sandbox.1self.co (can be updated to live url when ready)
IBEACON_UUID=<UUID for attached beacon>
IBEACON_MAJOR=<major value for attached beacon>
IBEACON_MINOR=<minor value for attached beacon>
APP_NAME=<the name of your app>
APP_VERSION=0.1 <keep your version updated>
```
