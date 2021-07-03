import numpy as np
import matplotlib.pyplot as plt
import pandas as ps

class lecture():
    """Lecture class. Creates an object for one single lecture."""


    def __init__(self, dataframe):
        """
        Initialise the lecture object. Requires a pandas DataFrame
        containing the following information:
        Data required for the on site consumption:
        - Electronic device usage
        - Air conditioning
        - Lighting
        - Beamer
        - Transportation
        Data for the online lectures:
        - Streaming
        - Electronic device usage
        - Lighting

        Parameters
        ----------
        dataframe : pandas DataFrame or Dict

        """

        if dataframe is None:
            raise ValueError("No data supplied to create lecture. Please supply data.")

        try:
            self.electronic_online = dataframe["ElectronicOnline"]
        except KeyError:
            self.electronic_online = None
        try:
            self.electronic_onsite = dataframe["ElectronicOnsite"]
        except KeyError:
            self.electronic_onsite = None
        try:
            self.air_conditioning = dataframe["AirConditioning"]
        except KeyError:
            self.air_conditioning = None
        try:
            self.streaming = dataframe["Streaming"]
        except KeyError:
            self.streaming = None
        try:
            self.transportation = dataframe["Transportation"]
        except KeyError:
            self.transportation = None
        try:
            self.lighting_online = dataframe["LightingOnline"]
        except KeyError:
            self.lighting_online = None
        try:
            self.lighting_onsite = dataframe["LightingOnsite"]
        except KeyError:
            self.lighting_onsite = None
        try:
            self.beamer = dataframe["Beamer"]
        except KeyError:
            self.beamer = None

        return

    def check_onsite(self):
        """Check if all variables for the calculation of the onsite model are present"""
        if self.electronic_onsite is None:
            return False
        elif self.air_conditioning is None:
            return False
        elif self.transportation is None:
            return False
        elif self.beamer is None:
            return False
        else:
            return True


    def check_online(self):
        """Check if all variables for the calculation of the online model are present"""
        if self.electronic_online is None:
            return False
        elif self.streaming is None:
            return False
        elif self.lighting_online is None:
            return False
        else:
            return True


    def caluclate_onsite(self):
        """Function to calculate the onsite model"""
        pass


    def plot_onsite(self):
        """Function to create the plot of the onsite model"""
        pass


    def calculate_online(self):
        """Function to calculate online model"""
        pass


    def plot_online(self):
        """Function to create the plot of the online model"""