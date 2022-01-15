import warnings

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import corner

from .models import *

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
        - options
            List of str conatining all selected options
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
            elif key == "options":
                self.options = value
            else:
                warnings.warn("Unrecognized key '%s', ignoring..." % key)

        return

    def get_random_living_consumption(self, living_list, living_random_length=100):
        """
        Gets a randomised value for the consumption of the living arrangements
        """
        cons = []
        l_cons = []
        for l in living_list:
            l_cons.append(l.get_consumption())
        indices = np.arange(len(l_cons))
        for i in range(living_random_length):
            rnd_cons = 0
            choices = np.random.choice(indices, self.num_stud)
            for choice in choices:
                rnd_cons += l_cons[choice]
            cons.append(rnd_cons)
        # Use median instead of mean in case of tailed distribution
        return np.median(cons), np.std(cons)

    def get_random_device_consumption(
        self, device_list, dev_stat, sampling="simple", device_random_length=100
    ):
        cons = []
        d_cons = []
        for d in device_list:
            d_cons.append(d.get_consumption())
        # TODO get proper kernel
        kernel = stats.gaussian_kde(dev_stat)
        if sampling == "simple":
            for i in range(device_random_length):
                rnd_cons = 0
                choices = np.rint(kernel.resample(self.num_stud)[0]) % len(d_cons)
                for choice in choices:
                    rnd_cons += d_cons[int(choice)]
                cons.append(rnd_cons)
        elif sampling == "mcmc":
            if emcee is None:
                raise ImportError("Emcee not imported")

            def log_prob(x):
                return kernel.logpdf(x)

            ndim, nwalkers = 1, self.num_stud
            p0 = np.random.randn(nwalkers, ndim)

            sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
            sampler.run_mcmc(p0, 1000)
            samples = np.rint(sampler.get_chain(flat=True)[:, 0]) % len(d_cons)
            for i in range(device_random_length):
                random_samples = np.random.choice(
                    np.arange(len(samples)), self.num_stud
                )
                choices = samples[random_samples]
                rnd_cons = 0
                for choice in choices:
                    rnd_cons += d_cons[int(choice)]
                cons.append(rnd_cons)
        return np.median(cons), np.std(cons)

    def get_random_transportation_consumption(
        self,
        transport_list,
        mot,
        t_dur,
        t_freq,
        lec_pw,
        sampling="simple",
        transport_random_length=100,
    ):
        cons = []
        t_cons = []
        t_conv = []
        for t in transport_list:
            t_cons.append(t.get_consumption())
            t_conv.append(t.transport_dist)
        # TODO get proper kernel
        
        kernel = stats.gaussian_kde(
            np.vstack([mot, t_dur, t_freq, lec_pw])
        )

        if sampling == "simple":
            for i in range(transport_random_length):
                rnd_cons = 0
                choices, duration, freq, lpw = kernel.resample(self.num_stud)
                choices = np.rint(choices)
                for j, choice in enumerate(choices):
                    rnd_cons += t_cons[int(choice)] * t_conv[int(choice)] * duration[j] * freq[j] / lpw[j]  
                cons.append(rnd_cons)
        elif sampling == "mcmc":
            if emcee is None:
                raise ImportError("Emcee not imported")

            def log_prob(x):
                return kernel.logpdf(x)

            ndim, nwalkers = 4, self.num_stud
            p0 = np.random.randn(nwalkers, ndim)

            sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
            sampler.run_mcmc(p0, 1000)
            samples = sampler.get_chain(flat=True)
            for i in range(transport_random_length):
                random_samples = np.random.choice(
                        np.arange(len(samples[:,0])), self.num_stud
                )
                choices, duration, freq, lpw = samples[random_samples].T
                choices = np.rint(choices) % len(t_cons)
                rnd_cons = 0
                for j, choice in enumerate(choices):
                    rnd_cons += t_cons[int(choice)] * t_conv[int(choice)] * duration[j] * freq[j] / lpw[j]  
                cons.append(rnd_cons)

        return np.median(cons), np.std(cons)

    def get_consumption(
        self,
        mode,
        sampling="simple",
        living_random_length=100,
        device_random_length=100,
        transport_random_length=100,
    ):
        """
        Basic function to get the consumption of a lecture

        Parameters
        ----------
        mode : str
            Determines mode of lecture. Recognised modes:
            offline, online-streaming, online-vod,
            hybrid-streaming, hybrid-vod.
        sampling : str
            Method for samling. Either 'simple' or 'mcmc'.
        living_random_length : int
            Number of randomised draws for the living situation
        device_random_length : int
            Number of randomised draws for the devices
        transport_random_length : int
            Number of randomised draws for the transportation


        Returns
        -------
        consumption : float
            Consumption of lecture in kW
        stat_uncertainty : float
            Statistical uncertainty from sampling procedure in kWh

        """

        # Check if lecture format is specified correctly
        if mode not in [
            "online-streaming",
            "online-vod",
            "offline",
            "hybrid-streaming",
            "hybrid-vod",
        ]:
            raise ValueError("Specified lecture format not recognized")

        # Check if emcee could be imported if sampling is set to mcmc
        if sampling not in ["simple", "mcmc"]:
            raise ValueError("Specified sampling mode not recognized")
        if sampling == "mcmc" and emcee is None:
            raise ImportError(
                "Sampling is set to mcmc, but emcee could not be imported"
            )

        # TODO remove Test output
        #### This output is a DUMMY until function is complete
        if mode == "hybrid-streaming":
            return np.random.rand(1)[0] * 40 * self.num_stud, 0
        elif mode == "hybrid-vod":
            return np.random.rand(1)[0] * 40 * self.num_stud, 0

        if mode == "online-streaming" or mode == "online-vod":
            # Calculation of the consumption for an online lecture
            # TODO Make sure that the calculation makes sense

            # Streaming service
            if mode == "online-streaming":
                if self.streaming is None:
                    # TODO Redirect to proper error page
                    raise AttributeError("Streaming service not set")
                # TODO Implemet correct function call
                consumption = self.streaming.get_consumption()
            elif mode == "online-vod":
                if self.vod is None:
                    # TODO Redirect to proper error page
                    raise AttributeError("VoD service not set")
                # TODO Implemet correct function call
                consumption = self.vod.get_consumption()
            stat_uncertainty = 0

            # Living situation
            if self.living is None:
                # Get randomised living situations
                living_list = Living_Situation.objects.order_by("living_name")
                if "random_living" in self.options:
                    c, s = self.get_random_living_consumption(
                        living_list, living_random_length=living_random_length
                    )
                    consumption += c
                    stat_uncertainty += s ** 2
                else:
                    for l in living_list:
                        l.get_consumption() * self.num_stud / len(living_list)
            else:
                consumption += self.living.get_consumption() * self.num_stud

            # Electronic devices
            if self.device is None:
                # Get randomised devices
                device_list = Electronic_Device.objects.order_by("device_name")
                if "random_device" in self.options:
                    dev_stat = np.arange(len(device_list))
                    c, s = self.get_random_device_consumption(
                        device_list,
                        dev_stat,
                        sampling=sampling,
                        device_random_length=device_random_length,
                    )
                elif self.faculty is not None:
                    if self.faculty.elec_dev_type_file is not None:
                        dev_stat = self.faculty.get_device_type_statistics()
                        c, s = self.get_random_device_consumption(
                            device_list,
                            dev_stat,
                            sampling=sampling,
                            device_random_length=device_random_length,
                        )
                    else:
                        dev = self.faculty.elec_dev_type
                        c = dev.get_consumption() * self.num_stud
                else:
                    raise AttributeError("Faculty must be selected")
                consumption += c
                stat_uncertainty += s ** 2
            else:
                consumption += self.device.get_consumption() * self.num_stud

            return consumption, np.sqrt(stat_uncertainty)

        if mode == "offline":
            # Lecture Hall
            if "beamer" in self.options:
                beamer = True
            else:
                beamer = False

            time = self.faculty.lec_length

            consumption = self.hall.get_consumption(time, beamer=beamer)
            stat_uncertainty = 0

            # Transportation
            transport_list = Transportation.objects.filter(
                university=self.university
            ).order_by("transport_name")

            mot, t_dur, t_freq = self.university.get_transport_statistics()
            lec_pw = self.faculty.get_lecture_statistics()
            c, s = self.get_random_transportation_consumption(
                transport_list,
                mot,
                t_dur,
                t_freq,
                lec_pw=lec_pw,
                sampling=sampling,
                transport_random_length=transport_random_length,
            )

            consumption += c
            stat_uncertainty += s ** 2

            # Electronic devices
            num_stud_bak = self.num_stud
            self.num_stud = int(np.rint(num_stud_bak * self.faculty.dev_usage))
            if self.device is None:
                # Get randomised devices
                device_list = Electronic_Device.objects.order_by("device_name")
                if "random_device" in self.options:
                    dev_stat = np.arange(len(device_list))
                    c, s = self.get_random_device_consumption(
                        device_list,
                        dev_stat,
                        sampling=sampling,
                        device_random_length=device_random_length,
                    )
                elif self.faculty is not None:
                    if self.faculty.elec_dev_type_file is not None:
                        dev_stat = self.faculty.get_device_type_statistics()
                        c, s = self.get_random_device_consumption(
                            device_list,
                            dev_stat,
                            sampling=sampling,
                            device_random_length=device_random_length,
                        )
                    else:
                        dev = self.faculty.elec_dev_type
                        c = dev.get_consumption() * self.num_stud
                else:
                    raise AttributeError("Faculty must be selected")
                consumption += c
                stat_uncertainty += s ** 2
            else:
                consumption += self.device.get_consumption() * self.num_stud

        self.num_stud = num_stud_bak

        return consumption, np.sqrt(stat_uncertainty)

