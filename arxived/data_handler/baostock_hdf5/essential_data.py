from typing import Optional
import pandas as pd

class HDF5DataFrameHandler():
    
    def __init__(self,path_hdf5file:Optional[str]=None,key_hdf5:Optional[str]=None,data_frame:Optional[pd.DataFrame]=None) -> None:
        if path_hdf5file is None and data_frame is None:
            raise ValueError("path_hdf5file and data_frame cannot be both None")
        if path_hdf5file is not None and data_frame is not None:
            raise ValueError("path_hdf5file and data_frame cannot be both set")
        if path_hdf5file is not None and key_hdf5 is None:
            raise ValueError("key_hdf5 should be set when path_hdf5file is set")
        if path_hdf5file is not None:
            self.data_frame = pd.read_hdf(path_hdf5file,key=key_hdf5)
        else:
            self.data_frame = data_frame