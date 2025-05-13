# analysis/post_analysis.py

import numpy as np
import matplotlib.pyplot as plt
from core.mycel import Mycel
from core.section import Section
from core.point import MPoint

import matplotlib.pyplot as plt
import numpy as np
from core.mycel import Mycel

def analyse_branching_angles(mycel: Mycel, save_path=None, csv_path=None):
    import matplotlib.pyplot as plt

    angles = []
    for section in mycel.get_all_segments():
        for child in section.children:
            if section.orientation and child.orientation:
                dot = section.orientation.dot(child.orientation)
                dot = max(min(dot, 1.0), -1.0)  
                angle_rad = np.arccos(dot)
                angles.append(np.degrees(angle_rad))

    if not angles:
        print("⚠️ No branching angles to analyse.")
        return

    mean_angle = np.mean(angles)
    print(f"📐 Mean branching angle: {mean_angle:.2f}°")

    if save_path:
        plt.figure()
        plt.hist(angles, bins=20, color='royalblue')
        plt.title("Branching Angle Distribution")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"📊 Branching angle histogram saved to {save_path}")

    if csv_path:
        import csv
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["BranchingAngleDegrees"])
            for angle in angles:
                writer.writerow([angle])
        print(f"📄 Branching angles exported to {csv_path}")

def vector_angle_deg(v1, v2):
    """Returns angle in degrees between two vectors."""
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    dot = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    return np.degrees(np.arccos(dot))

def analyse_tip_orientations(mycel: Mycel, save_path=None, csv_path=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  

    tips = mycel.get_tips()
    if not tips:
        print("⚠️ No tips to visualise orientations.")
        return

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Tip Orientation Vectors")

    orientations = []

    for tip in tips:
        x, y, z = 0, 0, 0
        u, v, w = tip.orientation.coords
        orientations.append((u, v, w))
        ax.quiver(x, y, z, u, v, w, length=1.0, normalize=True, color="purple")

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"🧭 Saved tip orientation histogram to {save_path}")

    if csv_path:
        import csv
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["X", "Y", "Z"])
            for u, v, w in orientations:
                writer.writerow([u, v, w])
        print(f"📄 Orientation vectors exported to {csv_path}")
