import os
import json
from skimage import io


class ScoringService(object):
    @classmethod
    def get_model(cls, model_path, reference_path, reference_meta_path):
        """Get model method

        Args:
            model_path (str): Path to the trained model directory.
            reference_path (str): Path to the reference data.
            reference_meta_path (str): Path to the meta data.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        try:
            cls.model = None
            cls.reference = os.listdir(reference_path)
            with open(reference_meta_path) as f:
                cls.reference_meta = json.load(f)

            return True
        except:
            return False


    @classmethod
    def predict(cls, input):
        """Predict method

        Args:
            input (str): path to the image you want to make inference from

        Returns:
            dict: Inference for the given input.
        """
        # load an image and get the file name
        image = io.imread(input)
        sample_name = os.path.basename(input).split('.')[0]

        # make prediction
        prediction = cls.reference[:10]

        # make output
        output = {sample_name: prediction}

        return output
