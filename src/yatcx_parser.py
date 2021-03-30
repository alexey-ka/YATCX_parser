"""
Advanced parser for the Garmin tcx files.
Influenced by python-tcxparser that focuses on the general session overview
Due to the expected high load to the parser, all the values are temporarily saved in-memory by default
"""
from datetime import datetime
import numpy as np
from lxml import objectify
from .exfunc import elem2dict, interpolate_nans, calculate_grade_arcsin
from .config import date_format, default_params, NSMAP


class TcxParser:
    def __init__(self, file_name, pre_read=False, params=default_params, recovery: bool = True):
        params['recovery'] = recovery
        self.__tree = objectify.parse(file_name)
        self.__root = self.__tree.getroot()
        self.__activity = self.__root.Activities.Activity
        self.__params = params

        self.__power_values = None
        self.__distance_values = None
        self.__speed_values = None
        self.__high_altitude_distance_value = None
        self.__elevations_values = None
        self.__grades_values = None
        self.__start_time = None
        self.__heart_rate = None
        self.__altitude_values = None
        if pre_read:
            self.__power_values = self.powers
            self.__distance_values = self.distances
            self.__speed_values = self.speeds
            self.__high_altitude_distance_value = self.high_altitude_distance

    @property
    def features(self):
        """ Get dictionary of all the available features"""
        r = elem2dict(self.__activity)
        return r

    @property
    def date(self):
        """Get date of the session"""
        return self.datetime.date()

    @property
    def datetime(self):
        """Get timestamp of the session start time"""
        if self.__start_time is None:
            session_date = datetime.strptime(
                str(self.__root.xpath("//ns:Id", namespaces=NSMAP)[0]).replace('T', ' ').replace('Z', ''), date_format)
            self.__start_time = session_date
        return self.__start_time

    @property
    def has_powers(self):
        """ Identify if the files include the power metrics"""
        if np.count_nonzero(np.isnan(self.powers)) == len(self.powers):
            return False
        return True

    @property
    def powers(self):
        if self.__power_values is None:
            self.__power_values = self.read_xpath_property(
                self.__root.xpath("//ns:Extensions/ns3:TPX", namespaces=NSMAP),
                'Watts')
            if self.__params['recovery']:
                self.__power_values = interpolate_nans(self.__power_values)
        return self.__power_values

    def mean_power_interval(self, interval):
        return np.convolve(self.powers, np.ones(interval), 'valid') / interval

    @property
    def grades(self):
        if self.__grades_values is None:
            self.__grades_values = []
            for elevation, move in zip(self.elevations, self.moves):
                if move > 0:
                    sin_value = elevation / move
                    if elevation / move > 1:
                        sin_value = np.nan

                    self.__grades_values.append(sin_value)
                else:
                    self.__grades_values.append(np.nan)

            if self.__params['recovery']:
                self.__grades_values = interpolate_nans(self.__grades_values)
            self.__grades_values = calculate_grade_arcsin(self.__grades_values)
        return self.__grades_values

    @property
    def distances(self):
        if self.__distance_values is None:
            self.__distance_values = [float(x.text) for x in
                                      self.__root.xpath("//ns:Trackpoint/ns:DistanceMeters", namespaces=NSMAP)]
            if self.__params['recovery']:
                self.__distance_values = interpolate_nans(self.__distance_values)
        return self.__distance_values

    @property
    def moves(self):
        return np.array(self.distances[1:] + [self.distances[-1]]) - np.array(self.distances)

    @property
    def low_altitude_distance(self):
        return self.total_distance - self.high_altitude_distance

    @property
    def high_altitude_distance(self):
        if self.__high_altitude_distance_value is None:
            self.__high_altitude_distance_value = np.sum(
                [move if elevation >= self.__params['high_altitude'] else 0 for move, elevation in
                 zip(self.moves, self.altitudes)])
        return self.__high_altitude_distance_value

    @property
    def elevations(self):
        if self.__elevations_values is None:
            self.__elevations_values = []
            zip_object = zip(self.altitudes[1:] + [self.altitudes[-1]], self.altitudes)
            for list1_i, list2_i in zip_object:
                if list1_i - list2_i > 0:
                    self.__elevations_values.append(list1_i - list2_i)
                else:
                    self.__elevations_values.append(0)
            if self.__params['recovery']:
                self.__elevations_values = interpolate_nans(self.__elevations_values)
        return self.__elevations_values

    @property
    def total_elevation(self):
        return np.sum(x if x > 0 else 0 for x in self.elevations)

    @property
    def heart_rate(self):
        if self.__heart_rate is None:
            self.__heart_rate = self.read_xpath_property(
                self.__root.xpath("//ns:HeartRateBpm", namespaces=NSMAP),
                'Value')
        return self.__heart_rate

    @property
    def mean_heart_rate(self):
        return self.__root.xpath("//ns:Lap/ns:AverageHeartRateBpm/ns:Value", namespaces=NSMAP)[0]

    @property
    def speeds(self):
        if self.__speed_values is None:
            self.__speed_values = self.read_xpath_property(
                self.__root.xpath("//ns:Extensions/ns3:TPX", namespaces=NSMAP),
                'Speed')
            if self.__params['recovery']:
                self.__speed_values = interpolate_nans(self.__speed_values)

        return self.__speed_values

    @property
    def altitudes(self):
        if self.__altitude_values is None:
            self.__altitude_values = list(
                [float(x) for x in self.__root.xpath("//ns:Trackpoint/ns:AltitudeMeters", namespaces=NSMAP)])
            if self.__params['recovery']:
                self.__altitude_values = interpolate_nans(self.__altitude_values)
        return self.__altitude_values

    @property
    def cadences(self):
        if self.__params['recovery']:
            return interpolate_nans([float(x.text) for x in self.__root.xpath("//ns:Cadence", namespaces=NSMAP)])
        return list([float(x.text) for x in self.__root.xpath("//ns:Cadence", namespaces=NSMAP)])

    @property
    def high_altitude_time(self):
        return np.sum([1 if x >= self.__params['high_altitude'] else 0 for x in self.altitudes])

    @property
    def total_distance(self):
        return self.__root.xpath("//ns:Lap/ns:DistanceMeters", namespaces=NSMAP)[0]

    @property
    def calories(self):
        return self.__root.xpath("//ns:Lap/ns:Calories", namespaces=NSMAP)[0]

    @property
    def total_time(self):
        return self.__root.xpath("//ns:Lap/ns:TotalTimeSeconds", namespaces=NSMAP)[0]

    def get_path(self, path, namespace):
        """ Read a random path if the given namespace"""
        return self.__root.xpath(path, namespaces=namespace)[0]

    def read_xpath_property(self, xpath_obj, name):
        """ Read a numeric property name in the given xpath_obj object"""
        res = np.array([float(x[name]) if hasattr(x, name) else np.nan for x in xpath_obj])
        return list(res)
