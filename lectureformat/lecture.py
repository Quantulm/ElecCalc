import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import emcee
import corner


class Lecture:
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
        try:
            self.num_lec = dataframe["NumLec"]
        except KeyError:
            self.num_lec = None

        self.onsite_sampler = None
        self.online_sampler = None

        return

    def get_onsite(self):
        """Function returning all data classified as 'onsite' data"""
        return np.array(
            [
                self.electronic_onsite,
                self.air_conditioning,
                self.transportation,
                self.lighting_onsite,
                self.beamer,
                self.num_lec,
            ]
        )

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
        elif self.num_lec is None:
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
        elif self.num_lec is None:
            return False
        else:
            return True

    def sample_onsite(self):
        """Function to resample data from onsite dataset"""

        # Step 1: Check if all data is present
        if not self.check_onsite():
            raise ValueError("Not enough data present for the calculation of the onsite result.")

        # Step 2: Create covariance matrix and mean vector
        data = self.get_onsite()

        cov = np.cov(data)

        mean = np.mean(data, axis=1)

        # Step 3: Define multivariate Gaussian density
        def log_prob(x, mean, cov):
            diff = x - mean
            return -0.5 * np.dot(diff, np.linalg.solve(cov, diff))

        # Step 4: Set up ensemble sampler
        nwalkers = 32
        ndim = len(mean)

        p0 = np.random.rand(nwalkers, ndim) # Initial value

        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, args=[mean, cov])

        # Step 5: Run a short burn in
        state = sampler.run_mcmc(p0, 100)
        sampler.reset()

        # Step 6: Run production
        sampler.run_mcmc(state, 5000)

        self.onsite_sampler = sampler

        return

    def caluclate_onsite(self):
        """Function to calculate the onsite model"""

        # Step 1: Check if data has been resampled and run sampler if not
        if self.onsite_sampler is None:
            self.sample_onsite()

        # Step 2: Sum up data to get total energy consumption
        flat_samples = self.onsite_sampler.get_chain(discard=100, thin=15, flat=True)

        return


    def plot_onsite(self):
        """Function to create the plot of the onsite model"""
        flat_samples = self.onsite_sampler.get_chain(discard=100, thin=15, flat=True)

        fig = corner.corner(
            flat_samples
        )

        return fig

    def calculate_online(self):
        """Function to calculate online model"""
        pass

    def plot_online(self):
        """Function to create the plot of the online model"""
