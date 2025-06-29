
import h5py


def write_h5(filename, im_data, metadata=None):

    with h5py.File(filename, 'w') as fh:

        if "image_data" in fh.keys():  del fh["image_data"]

        dset = fh.create_dataset("image_data", data=im_data , compression="gzip" )

        if metadata is not None:
            for key in metadata:
              dset.attrs[key] = list(metadata[key])