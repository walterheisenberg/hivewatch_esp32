from machine import Pin, enable_irq, disable_irq, idle

# für die China-Waage
# sc.set_scale(11.026667)
# sc = HX711(0,2)
# OFFSET = 130748.3 # witout wooden board
# middle: 130800
# SCALE = 11.026667

# some infos about lowpass filter:
# https://microsoft.public.de.excel.narkive.com/PNakkyeu/tiefpassfilter
# https://github.com/geda/hx711-lopy

class HX711:
    def __init__(self, dout, pd_sck, gain=128):

        self.pSCK = Pin(pd_sck , mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.pSCK.value(False)

        self.GAIN = 0
        #self.OFFSET = 0
        self.OFFSET = 130800
        
        #self.SCALE = 1
        self.SCALE = 11.026667

        #self.time_constant = 0.1
        self.time_constant = 0.9 # use 0.9 to get more responsive values, 0.1 means more filtered
        self.filtered = 0

        self.set_gain(gain);

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.read()
        self.filtered = self.read()
        print('Gain & initial value set')
    
    def is_ready(self):
        return self.pOUT() == 0

    def read(self):
        # wait for the device being ready
        while self.pOUT() == 1:
            idle()

        # shift in data, and gain & channel info
        result = 0
        for j in range(24 + self.GAIN):
            state = disable_irq()
            self.pSCK(True)
            self.pSCK(False)
            enable_irq(state)
            result = (result << 1) | self.pOUT()

        # shift back the extra bits
        result >>= self.GAIN

        # check sign
        if result > 0x7fffff:
            result -= 0x1000000

        return result

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def read_lowpass(self):
        print('self.filtered before: ' + str(self.filtered))
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return self.filtered

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def get_avgkg(self, times=3):
        return round( self.get_value(times) / self.SCALE / 1000 ,2 )

    def get_lpkg(self):
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return round( (self.filtered  - self.OFFSET)  / self.SCALE / 1000 ,2 )

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)
        print('OFFSET = ' + str(sum))

    def set_scale(self, scale = None):
        if scale is None:
            return self.SCALE
        self.SCALE = scale

    def set_offset(self, offset = None):
        if offset is None:
            return self.OFFSET
        self.OFFSET = offset

    def set_time_constant(self, time_constant = None):
        if time_constant is None:
            return self.time_constant
        elif 0 < time_constant < 1.0:
            self.time_constant = time_constant

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)

