import warnings

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import emcee
import corner


class Lecture:
    """Lecture class. Creates an object for one single lecture."""

    def __init__(self, num_stud, online, **kwargs):
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
        All other relevant information will be automatically
        retrieved from the database based on survey statistics

        Parameters
        ----------
        num_stud : int
            Number of students expected to attend the lecture
        """

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
            # TODO add remaining fields
            else:
                warnings.warn("Unrecognized key '%s', ignoring..." % key)

        return

    def get_consumption(online, sampling="simple"):
        """
        Basic function to get the consumption of a lecture

        Parameters
        ----------
        online : bool
            True of lecture is held online, False if offline
            (i.e. on-site)
        sampling : str
            Method for samling. Either 'simple' or 'mcmc'.

        Returns
        -------
        consumption : float
            Consumption of lecture in kW

        """
        
        # TODO remove Test output
        #### This output is a DUMMY until function is complete
        if online:
            return 8000
        else:
            return 6000

        if online:
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
