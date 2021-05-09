import numpy as np
import matplotlib.pyplot as plt
import io


def toycalc(sel_num_stud, lec_type, season):
        # Prototype model, most contributions are placeholders/ made up numbers
        num_students = np.arange(501, step=1)
        lec_type = lec_type/100

        # List different contributions, c.f. model PDF for informations
        # First value is on-site, second is online
        # All values in kWh
        A1 = np.array([25, 25]) # Electronic devices
        A2 = np.array([18, 0]) # Air conditioning
        A3 = np.array([0, 0.1152]) # Streaming
        A4 = np.array([86.4, 0]) # Transportation
        A5 = np.array([5.76, 4.32]) # Lighting
        A6 = np.array([0, 216]) # Beamer

        # Coefficients
        a1 = np.array([num_students * lec_type, num_students])
        a2 = np.array([season, 0])
        a3 = np.array([0, num_students])
        a4 = np.array([num_students, 0])
        a5 = np.array([1, num_students])
        a6 = np.array([1, 0])

        # Calculation of on-site and online consumption
        energy_on_site = a1[0] * A1[0] + a2[0] * A2[0] + a3[0] * A3[0] + a4[0] * A4[0] + a5[0] * A5[0] + a6[0] * A6[0]
        energy_online = a1[1] * A1[1] + a2[1] * A2[1] + a3[1] * A3[1] + a4[1] * A4[1] + a5[1] * A5[1] + a6[1] * A6[1]

        c_hyb = [0.2, 0.4, 0.6, 0.8] # Percentage of lectures being online
        energ_cons = []
        for c in c_hyb:
            energ_cons.append(c*energy_online + (1-c)*energy_on_site)
        
        res = "PLACEHOLDER"
        
        fig = plt.figure()
        for c in c_hyb:
            plt.plot(num_students, c*energy_online + (1-c)*energy_on_site, label=r"C$_{online}$=%s" % str(c))
        ymin = plt.gca().get_ylim()[0]
        ymax = plt.gca().get_ylim()[1]
        plt.vlines(sel_num_stud, ymin, ymax, label="Selected number of students", color="red", linestyle="--")

        plt.xlabel("Number of Students")
        plt.ylabel("Energy consumption (kWh)")
        plt.legend()
        plt.title("Hybrid lectures")

        imgdata = io.StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        
        return data, res


# Function call for debugging
if __name__ == "__main__":
    toycalc(200, 20, 0)