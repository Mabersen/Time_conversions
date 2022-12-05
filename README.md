# Time_conversions
This script contains functions which allow you to convert between utc, ut1 and tai time.
Modules required to run:
  -python datetime
  -julian
  -numpy
  -pandas
  -urllib
  -os
 
 There are four functions contained within the script, these are:
 
  -get_time_conversion_tables(): this function retrieves the current utc-uti time conversion tables from https://maia.usno.navy.mil/ser7/finals2000A.daily , extracts the important information and formats it for use later on. Use this if you only wish to view the conversion table data.
  
  -get_leap_second_value(): This retrieves the current number of added leap seconds from https://maia.usno.navy.mil/ser7/tai-utc.dat. This value is used to convert utc to tai.
  
 -utc2ut1(timelist): as the name implies, this converts from utc to ut1 time. The input is a list of python datetimes. This list is the datetimes you wish to convert to ut1 time.
 
 -utc2gps(datetime): This takes a datetime input and converts it to tai time by adding the current leapseconds.
