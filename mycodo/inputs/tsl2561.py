# coding=utf-8
import logging
from .base_input import AbstractInput

logger = logging.getLogger("mycodo.inputs.tsl2561")


class TSL2561Sensor(AbstractInput):
    """ A sensor support class that monitors the TSL2561's lux """

    def __init__(self, address, bus, testing=False):
        super(TSL2561Sensor, self).__init__()
        self._lux = None
        self.i2c_address = address
        self.i2c_bus = bus

        if not testing:
            from tentacle_pi import TSL2561
            self.tsl = TSL2561.TSL2561(
                self.i2c_address, "/dev/i2c-" + str(self.i2c_bus))

    def __repr__(self):
        """  Representation of object """
        return "<{cls}(lux={lux})>".format(cls=type(self).__name__,
                                           lux="{0:.2f}".format(self._lux))

    def __str__(self):
        """ Return lux information """
        return "Lux: {lux}".format(lux="{0:.2f}".format(self._lux))

    def __iter__(self):  # must return an iterator
        """ TSL2561Sensor iterates through live lux readings """
        return self

    def next(self):
        """ Get next lux reading """
        if self.read():  # raised an error
            raise StopIteration  # required
        return dict(lux=float('{0:.2f}'.format(self._lux)))

    @property
    def lux(self):
        """ TSL2561 luminosity in lux """
        if not self._lux:  # update if needed
            self.read()
        return self._lux

    def get_measurement(self):
        """ Gets the TSL2561's lux """
        self._lux = None
        self.tsl.enable_autogain()
        # tsl.set_gain(16)
        self.tsl.set_time(0x00)
        return self.tsl.lux()


    def read(self):
        """
        Takes a reading from the TSL2561 and updates the self._lux value

        :returns: None on success or 1 on error
        """
        try:
            self._lux = self.get_measurement()
            return  # success - no errors
        except Exception as e:
            logger.exception(
                "{cls} raised an exception when taking a reading: "
                "{err}".format(cls=type(self).__name__, err=e))
        return 1
