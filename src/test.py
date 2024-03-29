import numpy as np

from org.openehr.base.base_types.builtins import Env

from org.openehr.base.foundation_types.primitive_types import Uri
from org.openehr.base.foundation_types.interval import PointInterval
from org.openehr.base.foundation_types.time import ISOTimeZone

refA : Uri = Uri("http://google.com")
refB : Uri = Uri("http://google.coms")

print(refA == refA)

f = np.array([Uri("http://bbc.co.uk"), Uri("http://google.com")])
print(f[1])

s = {1, 2, 2}

d = {1: 42, 9: 31}

print(d[9])

i = PointInterval(np.int32(0))
i.lower = np.int32(29)

tz = ISOTimeZone("-12:00")
print(tz)
print(tz.to_python_timezone())

tz = Env.current_time_zone()
print(tz)
print(tz.is_gmt())
