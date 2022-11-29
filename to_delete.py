class TimeSequence:

    def __init__(self, ts_array):
        # A numpy array, usually of two dimensions. Rows correspond to joint angles; columns, to timesteps.
        self.ts_array = ts_array

    def get_ts_array(self):
        return self.ts_array

    def get_shape(self):
        print(self.ts_array.shape)
        return self.ts_array.shape

    def get_number_of_joints(self):
        return len(self.ts_array[0])

    def get_number_of_timesteps(self):
        return len(self.ts_array)

    def get_one_joint(self, index, verbose=False):  # index: from 0-th to n-th -1
        if verbose:
            print(self.ts_array[:, index])
        return self.ts_array[:, index]

    def plot_joints(self, *args):

        if len(args) == 0:
            utils.plot_joints(self.ts_array)
        else:
            selected_array = self.ts_array[:, list(args)]
            utils.plot_joints(selected_array)

    def downsampling(self, new_ts):
        self.ts_array = utils.downsampling(self.ts_array, new_ts)

    # Appends extra joints at the end, column-wise
    def add_joints(self, extra_joints):
        self.ts_array = utils.stack_seq_joints(self.ts_array, extra_joints)

    # Appends extra timesteps at the end, row-wise
    def add_timesteps(self, extra_ts):
        self.ts_array = utils.stack_seq_ts(self.ts_array, extra_ts)
        return self.ts_array


class Primitive(TimeSequence):

    # prim may be either a path to an .npy file, or a numpy array
    # variation: any kind of tag that the user may want to add, to distinguish similar primitives from each other
    def __init__(self, prim, *variation):
        if type(prim) == str:
            self.ts_array = io.npy_to_array(prim)
        else:
            self.ts_array = prim
        self.variation = variation

    def get_variation(self):
        return self.variation


# Useful when starting from single positions of the robot, rather than from trajectories
class Customized(Primitive):

    def __init__(self, *ts_array):
        if len(ts_array) == 0:
            self.ts_array = array([])
        else:
            self.ts_array = ts_array

    def get_array(self):
        print(self.ts_array)
        return self.ts_array

    # Repeat a still position many times, thus creating a "pause" trajectory
    # The argument must be a 2D array of one element (the angle of each joint, at a given timestep)
    def create_pause(self, ts):
        pos = self.ts_array
        self.ts_array = repeat(pos, ts, axis=0)
        return self.ts_array

    # Given two still positions, it creates a trajectory of length "ts" between the two positions
    # The interpolated points are equidistant from each other.
    def pos_interpolate(self, pos1, pos2, ts):
        self.ts_array = io.interpolate(pos1, pos2, ts)

