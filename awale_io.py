import os
from datetime import datetime

version = 0
save_dir = os.path.expanduser("~") + "/Awale/V{}/".format(version)


def save_model_and_df(model, df, gamma, epochs, memory_size, batch_size, comment):
    """
    Save a model and a dataframe
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save model
    name = get_save_name(gamma, epochs, memory_size, batch_size, comment)
    model.save(save_dir + name + ".model")

    # Save dataframe
    name = get_save_name(gamma, epochs, memory_size, batch_size, comment)
    df.to_hdf(save_dir + name + ".hdf5", 'name', complevel=9, complib='blosc')


def get_save_name(gamma, epochs, memory_size, batch_size, comment):
    """
    Get the save name corresponding to the arguments
    :return: name
    """
    name = "gamma-" + str(gamma)
    name += "-epochs-" + str(epochs)
    name += "-memory_size-" + str(memory_size)
    name += "-batch_size-" + str(batch_size)
    name += "-comment-" + str(comment).replace("-", "_")
    name += "-date-" + datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return name


def get_parameters(name: str):
    """
    Return the parameters of a name
    :param name: can be a path
    :return: gamma, epochs, memory_size, batch_size, comment
    """
    s = name.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]
    l = s.split("-")

    return int(l[l.index("gamma") + 1]), \
           int(l[l.index("epochs") + 1]), \
           int(l[l.index("memory_size") + 1]), \
           int(l[l.index("batch_size") + 1]), \
           l[l.index("comment") + 1]


def get_parameters_dict(name: str):
    gamma, epochs, memory_size, batch_size, comment = get_parameters(name)
    return {"gamma": gamma, "epochs": epochs, "memory_size": memory_size, "batch_size": batch_size, "comment": comment}


def get_pretty_name(*parameters):
    """
    Return pretty name
    :param: parameters: gamma, epochs, memory_size, batch_size, comment
    """
    return "Gamma {}; Epochs {}; Memory Size {}; Batch Size {}; Comment {}".format(*parameters)
