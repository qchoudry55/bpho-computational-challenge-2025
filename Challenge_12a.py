import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#white light enters triangular prism and bends towards normal
#when hits other side of prism, disperses into different wavelengths and colours of rainbow
#occurs due to different wavelengths having different refractive indices
#all bend away from normal when leaving

#wavelengths in nm and refractive indices in glass
wavelengths = np.array([700, 590, 570, 510, 450, 400])        #650, 590, 570, 510, 475, 445
n_glass = np.array([1.513, 1.517, 1.519, 1.523, 1.528, 1.550])
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']

#function for Snell's law
def snell(n1, n2, theta1):
    val = n1 / n2 * np.sin(theta1)
    val = np.clip(val, -1, 1)
    return np.arcsin(val)

#function for rays
def line_segment_intersect(p, d, seg_start, seg_end):
    v = seg_end - seg_start
    mat = np.column_stack((v, -d))
    try:
        t, s = np.linalg.solve(mat, p - seg_start)
        if 0 <= t <= 1 and s >= 0:
            return seg_start + t * v, s
        else:
            return None, None
    except np.linalg.LinAlgError:
        return None, None

#function for when light leaves prism and disperses into different wavelengths
def plot_prism_dispersion(incident_angle_deg, alpha_deg, ax):
    ax.clear()
    #define incident angle of original white light ray
    incident_angle = np.radians(incident_angle_deg)
    #define alpha (top angle of prism)
    alpha = np.radians(alpha_deg)

    #set prism vertices w/ adjustable apex angle
    A = np.array([0, 0])
    h = np.sqrt(0.25 * (1 + np.cos(alpha)) / (1 - np.cos(alpha)))
    #adjust height w/ alpha to allow for different angles
    C = np.array([0.5, h])
    B = np.array([1, 0])

    #plot prism
    prism_pts = np.array([A, C, B, A])
    ax.plot(prism_pts[:, 0], prism_pts[:, 1], 'k-', linewidth=2)

    #define prism face AC
    AC = C - A
    AC_len = np.linalg.norm(AC)
    AC_unit = AC / AC_len

    #draw normal to face AC pointing outside the prism
    normal_AC_out = np.array([-AC_unit[1], AC_unit[0]])

    #draw fixed beam start point at (0.25, 0.25)
    beam_start = np.array([-0.5, 0])

    c, s = np.cos(-incident_angle), np.sin(-incident_angle)
    R = np.array([[c, -s], [s, c]])
    beam_dir = R @ (-normal_AC_out)

    #if axes and light do not hit prism
    entry_pt, s_param = line_segment_intersect(beam_start, beam_dir, A, C)
    if entry_pt is None:
        ax.text(0.5, 0.5, "Beam misses prism face AC!", color='red', fontsize=14)
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.axis('off')
        return
    ax.plot([beam_start[0], entry_pt[0]], [beam_start[1], entry_pt[1]], 'k-', linewidth=3, label='Incoming White Light')
    ax.plot(entry_pt[0], entry_pt[1], 'ko')  # Entry point

    #calculate refracted angle inside prism for violet wavelength (max refraction)
    theta1 = incident_angle  # angle between beam and outside normal
    theta2_violet = snell(1.0, n_glass[-1], theta1)

    #direction inside prism beam vector
    face_angle_AC = np.arctan2(-normal_AC_out[1], -normal_AC_out[0])
    beam_inside_dir_angle = face_angle_AC - theta2_violet
    beam_inside_dir = np.array([np.cos(beam_inside_dir_angle), np.sin(beam_inside_dir_angle)])

    #prism face CB
    CB = B - C
    CB_len = np.linalg.norm(CB)
    CB_unit = CB / CB_len

    #find intersection with face CB inside prism
    exit_pt, s_exit = line_segment_intersect(entry_pt, beam_inside_dir, C, B)
    if exit_pt is None:
        ax.text(0.5, 0.5, "Beam misses prism face CB!", color='red', fontsize=14)
        ax.set_xlim(-1, 2)
        ax.set_ylim(-0.5, 2)
        ax.axis('off')
        return

    ax.plot(exit_pt[0], exit_pt[1], 'ko')  # Exit point

    #plot beam inside prism (violet)
    ax.plot([entry_pt[0], exit_pt[0]], [entry_pt[1], exit_pt[1]], color='purple', linewidth=3,
            label='Inside Prism (Violet)')

    #normal to face CB pointing outside prism
    normal_CB_out = np.array([-CB_unit[1], CB_unit[0]])

    #angle inside prism beam with face normal at exit
    angle_inside_face_CB = np.arccos(np.clip(np.dot(beam_inside_dir, -normal_CB_out), -1, 1))

    #angles for all different wavelengths
    for i, wl in enumerate(wavelengths):
        n = n_glass[i]

        normal_CB_out = np.array([-CB_unit[1], CB_unit[0]])
        if np.dot(normal_CB_out, A - C) < 0:
            normal_CB_out = -normal_CB_out

        beam_inside_dir = (exit_pt - entry_pt)
        beam_inside_dir /= np.linalg.norm(beam_inside_dir)

        normal_vec = normal_CB_out / np.linalg.norm(normal_CB_out)

        cos_theta_i = np.dot(beam_inside_dir, normal_vec)
        theta_i_exit = np.arccos(np.clip(cos_theta_i, -1, 1))

        sin_theta_t_exit = n * np.sin(theta_i_exit)

        # Handle total internal reflection by forcing maximum refraction angle
        if sin_theta_t_exit > 1.0:
            theta_t_exit = np.pi / 2
        else:
            theta_t_exit = np.arcsin(sin_theta_t_exit)

        normal_angle = np.arctan2(normal_vec[1], normal_vec[0])

        candidate1 = np.array([np.cos(normal_angle + theta_t_exit), np.sin(normal_angle + theta_t_exit)])
        candidate2 = np.array([np.cos(normal_angle - theta_t_exit), np.sin(normal_angle - theta_t_exit)])

        def cross_sign(v1, v2):
            return np.sign(v1[0] * v2[1] - v1[1] * v2[0])

        side_inside = cross_sign(beam_inside_dir, normal_vec)
        side_cand1 = cross_sign(candidate1, normal_vec)
        side_cand2 = cross_sign(candidate2, normal_vec)

        if side_cand1 != side_inside and np.dot(candidate1, normal_vec) > 0:
            exit_dir = candidate1
        elif side_cand2 != side_inside and np.dot(candidate2, normal_vec) > 0:
            exit_dir = candidate2
        else:
            dot1 = np.dot(candidate1, normal_vec)
            dot2 = np.dot(candidate2, normal_vec)
            exit_dir = candidate1 if dot1 > dot2 else candidate2

        #final ray leaving prism
        exit_dir /= np.linalg.norm(exit_dir)
        exit_dir = -exit_dir
        angle_offset = np.radians(-5 + 10 * i / (len(wavelengths) - 1))
        base_angle = np.arctan2(exit_dir[1], exit_dir[0])
        new_angle = base_angle + angle_offset
        exit_dir = np.array([np.cos(new_angle), np.sin(new_angle)])
        exit_beam_end = exit_pt + exit_dir * 1.5

        if colors[i] == 'violet' or 'blue' or 'red':
            lw = 1
        else:
            lw = 0.5
        ax.plot([exit_pt[0], exit_beam_end[0]], [exit_pt[1], exit_beam_end[1]], color=colors[i], linewidth=lw)

    #draw axes
    ax.set_xlim(-1, 2)
    ax.set_ylim(-0.5, 2)
    ax.set_xlabel('X position (arb. units)')
    ax.set_ylabel('Y position (arb. units)')
    ax.set_title('White Light Dispersion Through Prism (Apex Angle = {:.1f}°)'.format(alpha_deg))
    ax.grid(True)
    ax.legend(loc='upper right')

    plt.draw()

#create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)

#initial parameters for sliders
init_incident_angle = 30
init_alpha = 30
plot_prism_dispersion(init_incident_angle, init_alpha, ax)

#create sliders
ax_inc = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_alpha = plt.axes([0.2, 0.1, 0.6, 0.03])

slider_inc = Slider(ax_inc, 'Incident Angle (deg)', -180, 120, valinit=init_incident_angle)
slider_alpha = Slider(ax_alpha, 'Apex Angle (deg)', 30, 60, valinit=init_alpha)

#function to update plot when sliders are used
def update(val):
    plot_prism_dispersion(slider_inc.val, slider_alpha.val, ax)

#use update function for sliders
slider_inc.on_changed(update)
slider_alpha.on_changed(update)

plt.show()