import numpy as np
from django.test import TestCase
import pandas as pd
import lecture as lec
import matplotlib.pyplot as plt

# Create your tests here.
def lecture_test_onsite(n_student, frac):
    """Function to test lecture class onsite calculation"""

    rng = np.random.default_rng(seed=42) # Seed to ensure reproducability

    # Artificial covariance between numlec and transportation
    cov = np.array(
        [[ 20, -4.9],
        [-4.9,  1.9]]
    )
    corr_dat = rng.multivariate_normal(mean=[86.4, 5], cov=cov, size=n_student).T

    # Create test data set:
    A1 = np.array([25, 25])  # Electronic devices
    A2 = np.array([18, 0])  # Air conditioning
    A3 = np.array([0, 0.1152])  # Streaming
    A4 = np.array([86.4, 0])  # Transportation
    A5 = np.array([5.76, 4.32])  # Lighting
    A6 = np.array([0, 216])  # Beamer

    df = pd.DataFrame(
        {
            # "ElectronicOnline": np.full(shape=n_student, fill_value=25),
            "ElectronicOnline": rng.normal(loc=25, scale=5, size=n_student),
            "ElectronicOnsite": rng.normal(loc=25*frac, scale=5, size=n_student),
            "AirConditioning": rng.normal(loc=18, scale=1, size=n_student),
            # "AirConditioning": np.full(shape=n_student, fill_value=18),
            "Streaming": rng.normal(loc=0.1152, scale=0.01, size=n_student),
            # "Streaming": np.full(shape=n_student, fill_value=0.1152),
            "Transportation": corr_dat[0],
            "NumLec": corr_dat[1],
            "LightingOnline": rng.normal(loc=4.32, scale=0.5, size=n_student),
            # "LightingOnline": np.full(shape=n_student, fill_value=4.32),
            "LightingOnsite": rng.normal(loc=5.76, scale=0.5, size=n_student),
            # "LightingOnsite": np.full(shape=n_student, fill_value=5.76),
            "Beamer": rng.normal(loc=216, scale=10, size=n_student),
            # "Beamer": np.full(shape=n_student, fill_value=216),
        }
    )

    lecture = lec.lecture(df)

    lecture.caluclate_onsite()

    fig = lecture.plot_onsite()
    plt.show()


    return


def create_lecture(num):
    lect = lec.Lecture(500, tkey=300)
    print("created lecture")


def main():
    create_lecture(500)

if __name__ == "__main__":
    main()
