import warnings

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import corner

try:
    import emcee
except ImportError:
    emcee = None


class Lecture:
    """Lecture class. Creates an object for one single lecture."""

    def __init__(self, num_stud, **kwargs):
        """
        Initialise the lecture object.
        Requires number of students and format. Further information
        can be added via keywords.
        Possible keywords:
        - hall
            LectureHall object
        - streaming
            StreamingService object
        - vod
            VideoOnDemandService object
        - faculty
            Faculty object
        - university
            University object
        - living
            Living_Situation object
        - device
            Electronic_Device object
        - transport
            Transport object
        All other relevant information will be automatically
        retrieved from the database based on survey statistics

        Parameters
        ----------
        num_stud : int
            Number of students expected to attend the lecture
        """

        # Check if number of students is valid
        if num_stud < 0:
            raise ValueError(
                    "Show me a lecture with negative number of students attending"
            )
        else:
            self.num_stud = num_stud

        for key, value in kwargs.items():
            if key == "hall":
                self.hall = value
            elif key == "streaming":
                self.streaming = value
            elif key == "vod":
                self.vod = value
            elif key == "faculty":
                self.faculty = value
            elif key == "university":
                self.university = value
            elif key == "living":
                self.living = value
            elif key == "device":
                self.device = value
            elif key == "transport":
                self.transport = value
            else:
                warnings.warn("Unrecognized key '%s', ignoring..." % key)

        return

    def get_consumption(online, sampling="simple", max_onsite):
        """
        Basic function to get the consumption of a lecture

        Parameters
        ----------
        online : str
            Determines mode of lecture. Recognised modes:
            offline, online, hybrid.
        sampling : str
            Method for samling. Either 'simple' or 'mcmc'.
        max_onsite : int
            Maximum number of students allowed onsite. Has to be
            given when online="hybrid". Otherwise it is ignored.

        Returns
        -------
        consumption : float
            Consumption of lecture in kW

        """

        # Check if lecture format is specified correctly
        if online not in ["online", "offline", "hybrid"]:
            raise ValueError(
                    "Specified lecture format not recognized"
            )

        # Check is max_onsite is set for hybrid format
        if online == "hybrid" and max_onsite is None:
            raise AttributeError(
                "Lecture is specified as hybrid, but maximum number of onsite students is missing"
            )


        # Check if emcee could be imported if sampling is set to mcmc
        if sampling not in ["simple", "mcmc"]:
            raise ValueError(
                    "Specified sampling mode not recognized"
            )
        if sampling == "mcmc" and emcee is None:
            raise ImportError(
                "Sampling is set to mcmc, but emcee could not be imported"
            )

        # TODO remove Test output
        #### This output is a DUMMY until function is complete
        if online == "online":
            return np.random.rand(1)[0] * 60 * self.num_stud
        elif online == "offline":
            return np.random.rand(1)[0] * 50 * self.num_stud
        elif online == "hybrid":
            return np.random.rand(1)[0] * 40 * self.num_stud

        if online == "online":
            # Calculation of the consumption for an online lecture
            # TODO Make sure that the calculation makes sense

            # Get all available Living situation
            # TODO refine to only select living situations that are
            # relevant for selecte university
            livings = Living_Situation.objects.all()

            # Get all possible consumptions
            living_consumptions = []
            for l in living:
                living_consumptions.append(l.get_consumption())

            # TODO For simple sampling use kde.resample()

            return

            consumption = self.streaming.get_consumption(num_stud)
