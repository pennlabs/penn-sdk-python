import os
from penn import *

m = Map(os.getenv("NEM_USERNAME"), os.getenv("NEM_PASSWORD"))
d = Dining(os.getenv("DIN_USERNAME"), os.getenv("DIN_PASSWORD"))
t = Transit(os.getenv("TRANSIT_USERNAME"), os.getenv("TRANSIT_PASSWORD"))
